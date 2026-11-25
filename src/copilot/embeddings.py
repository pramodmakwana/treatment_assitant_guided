from google import genai
from google.genai import types
from langchain_core.embeddings import Embeddings

from copilot import config


class GeminiEmbeddings(Embeddings):
    """LangChain-compatible wrapper around Gemini embeddings."""

    def __init__(self, batch_size: int = 50):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.batch_size = batch_size

    def _embed(self, texts: list[str], task_type: str) -> list[list[float]]:
        vectors = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            result = self.client.models.embed_content(
                model=config.EMBED_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=config.EMBED_DIM,
                ),
            )
            vectors.extend(e.values for e in result.embeddings)
        return vectors

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts, "RETRIEVAL_DOCUMENT")

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text], "RETRIEVAL_QUERY")[0]
