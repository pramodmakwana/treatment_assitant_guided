import os

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gemini-3.5-flash")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "gemini-embedding-001")
EMBED_DIM = int(os.environ.get("EMBED_DIM", "768"))
PG_DSN = os.environ.get("PG_DSN", "postgresql+psycopg://tga:tga_local_pw@localhost:5432/guidelines")