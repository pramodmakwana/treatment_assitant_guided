from google import genai
from google.genai import types
from copilot import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

reply = client.models.generate_content(
    model=config.CHAT_MODEL,
    contents="In two sentences, what is 'structuring' in anti-money laundering?",
)
print("LLM:", reply.text)

emb = client.models.embed_content(
    model=config.EMBED_MODEL,
    contents=["Several cash deposits just under the EUR 10,000 threshold"],
    config=types.EmbedContentConfig(output_dimensionality=config.EMBED_DIM),
)
vector = emb.embeddings[0].values
print("Embedding length:", len(vector))
print("First 5 numbers:", [round(v, 4) for v in vector[:5]])
