import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_text_splitters import MarkdownHeaderTextSplitter

from copilot import config
from copilot.embeddings import GeminiEmbeddings

KB_DIR = Path(__file__).resolve().parents[2] / "knowledge_base"
COLLECTION = "protocols"
SECTION_ID = re.compile(r"^([A-Z0-9]+-\d+)\s+(.*)$")


def get_vector_store() -> PGVector:
    return PGVector(
        embeddings=GeminiEmbeddings(),
        collection_name=COLLECTION,
        connection=config.PG_DSN,
        use_jsonb=True,
    )


def load_and_split() -> list[Document]:
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "doc_title"), ("##", "section")]
    )
    chunks = []
    for path in sorted(KB_DIR.glob("*.md")):
        for doc in splitter.split_text(path.read_text()):
            section = doc.metadata.get("section", "")
            match = SECTION_ID.match(section)
            if not match:
                continue
            doc.metadata.update(
                source_file=path.name,
                section_id=match.group(1),
                section_title=match.group(2),
            )
            chunks.append(doc)
    return chunks


def main() -> None:
    chunks = load_and_split()
    print(f"Loaded {len(chunks)} sections from {KB_DIR}")
    store = get_vector_store()
    ids = [c.metadata["section_id"] for c in chunks]
    store.add_documents(chunks, ids=ids)
    print(f"Stored {len(ids)} chunks in collection {COLLECTION}")


if __name__ == "__main__":
    main()