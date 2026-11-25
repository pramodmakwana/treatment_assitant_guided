from copilot.ingest import get_vector_store

QUESTIONS = [
    "Can a patient with an eGFR of 25 start metformin?",
    "What should be checked after starting an ACE inhibitor?",
    "Which medicines should be paused during vomiting and diarrhoea?",
]

store = get_vector_store()
for q in QUESTIONS:
    print("\nQ:", q)
    for doc, score in store.similarity_search_with_score(q, k=3):
        print("  ", doc.metadata["section_id"], round(score, 3), doc.metadata["section_title"])