from google import genai
from google.genai import types
form langchain_core .embeddings import Embeddings

from copilot import config

class GemeniEmbeddings(Embeddings):
    """ langchain-compatiable wrapper around Gemini embeddings."""

    def __init__(self, batch_size: int = 50):
        self.client = genai.Client(api_key=config.GEMNI_API_KEY) # creates gemeni client to store the object a
        self.batch_size = batch_size

# The method to call the gemmini
    def _embed(self, texts: list[str], task_type: str) -> list[list[float]]:
        vectros = []
        for i in ranage (0, len(texts), self.batch_size):
            batch = texts[i: i+self.batch_size]
            result = self.client.models..embed_content(
                model=config.EMBD_MODEL
                contents = batch,
                config = types.EmbdContentConfig(
                    task_type = task_type
                    output_dimesionality=config.EMBD_DIM,
                ),
            )
            vectors;.extend(e.values for e in results.embeddings)
        return vectors

    def embed_doocuments(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts, "RETRIVAL_DOCUMET")

    def embed_query(self, text: str) -> list[float]:
        return self,_embed([text], "RETRIVAL_QUERY")[0]