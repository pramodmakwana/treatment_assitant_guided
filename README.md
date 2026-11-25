# Treatment Guideline Assistant

A GenAI clinical decision-support prototype that retrieves treatment protocol guidance for adults
with type 2 diabetes, hypertension and chronic kidney disease, checks drug-safety concerns, and drafts
cited treatment options for a clinician to review.

> **Disclaimer:** Portfolio prototype only. All patients are synthetic. The "Liffey Clinic" protocols are
> fictional and are not clinical guidance. This software is not a medical device and must not be used
> for real patient care.

## Why this project
Patients with several long-term conditions need treatment that follows each guideline while accounting
for how conditions and medicines interact (for example, kidney function changes which diabetes medicines
are appropriate). Clinicians must cross-check guidelines, current medicines and drug warnings in short
appointments. This assistant retrieves the relevant protocol sections, flags safety concerns and drafts
options with citations, while the clinician makes every decision.

**Design principle:** retrieval grounds the answer, code checks safety, the LLM drafts, the clinician decides.

## How it works

```
Protocol documents ─► split by section ─► Gemini embeddings ─► PostgreSQL + pgvector
                                                                     │
Clinician question ─► embed ─► similarity search ─► relevance threshold
                                                                     │
                              no relevant section ─► abstain (no LLM call)
                                                                     │
                              relevant sections ─► Gemini answer with [section] citations
                                                                     │
                                                    citation validation ─► clinician
```

Planned: a LangGraph workflow adding patient data, drug-safety checks (openFDA labels, kidney-function
rules), a validation loop and a clinician review step (interrupt/resume).

## Tech stack
| Area | Technology |
|------|------------|
| Language and tooling | Python, uv (locked dependencies), pytest |
| LLM and embeddings | Google Gemini (`gemini-3.5-flash`, `gemini-embedding-001`, 768 dimensions) |
| RAG framework | LangChain (text splitters, PGVector, structured output) |
| Workflow (planned) | LangGraph with Postgres checkpointer |
| Vector store | PostgreSQL 16 + pgvector (HNSW, cosine distance) via Docker Compose |
| Development environment | GitHub Codespaces (nothing installed locally) |
| Planned production | FastAPI, Streamlit review screen, Apache Airflow, Docker, GitHub Actions, Azure |

## Current status
| Requirement | Status |
|-------------|--------|
| Requirements, architecture and decision records (`docs/`) | Done |
| FR-01 Load, split, embed and store protocol sections (22 sections) | Done |
| FR-03 Retrieval by meaning (smoke test: correct section ranked first for 3/3 questions) | Done |
| FR-04 / SR-03 Cited answers with abstention and citation validation | In progress |
| FR-02 Synthetic patient data (Synthea) | Planned |
| FR-05 Drug-safety checks (openFDA, kidney rules) | Planned |
| FR-06 to FR-10 LangGraph workflow with clinician review and audit log | Planned |
| Evaluation and safety test suites | Planned |
| API, deployment and orchestration | Planned |

Results so far come from small smoke tests. A proper evaluation set, kept separate from the data used
to tune thresholds, is planned.

## Run it (GitHub Codespaces)
1. Add a Codespaces secret `GEMINI_API_KEY` (repo **Settings → Secrets and variables → Codespaces**).
2. Open a Codespace on `main`, then run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv sync
docker compose up -d
uv run python -m copilot.smoke_test     # check Gemini chat + embeddings
uv run python -m copilot.ingest         # load 22 protocol sections into pgvector
uv run python -m copilot.search_demo    # retrieval test
```

## Project structure
```
docs/                 requirements, architecture, architecture decision records
knowledge_base/       fictional Liffey Clinic protocols (one section = one chunk)
sql/init.sql          enables pgvector on first database start
src/copilot/
  config.py           settings from environment variables
  embeddings.py       Gemini embeddings adapter for LangChain (batching, task types)
  ingest.py           load, split, embed, store (idempotent upserts by section ID)
  search_demo.py      retrieval smoke test
  rag.py              cited answers with abstention (in progress)
docker-compose.yml    PostgreSQL + pgvector
pyproject.toml, uv.lock
```

## Safety approach
- Answers come only from retrieved protocol sections, with section citations that are validated in code.
- The assistant abstains when no section is relevant enough.
- No doses, no patient-facing advice, no diagnosis; safety flags ask the clinician to verify.
- Synthetic data only. The Gemini free tier may use prompts to improve Google products; a real
  deployment would use an enterprise endpoint with no training on patient data.

See [`docs/requirements.md`](docs/requirements.md) for the full safety and regulatory considerations
(EU MDR, EU AI Act, GDPR).

## Documentation
- [Requirements](docs/requirements.md)
- [Architecture](docs/architecture.md)
- [Architecture decision records](docs/adr.md)

## License
MIT