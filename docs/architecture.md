# Architecture: Treatment Guideline Assistant

**Status:** Draft v0.2

## 1. Overview

    Liffey Clinic protocols ─► load + split by section ─► embed (Gemini) ─► pgvector (LangChain PGVector)
    Synthetic patients (Synthea FHIR) ─► Postgres (conditions, medicines, labs, allergies)
    openFDA drug labels ─► Postgres (contraindications, drug interactions)   [refreshed nightly by Airflow]

                                   LangGraph workflow
    load_patient ─► retrieve_guidelines ─► evidence enough? ──no──► abstain
                                                 │ yes
                                                 ▼
                                      check_drug_safety (rules + labels)
                                                 ▼
                                      draft_options (Gemini, structured output)
                                                 ▼
                                      validate ──fail (max 2)──► draft_options
                                                 │ pass
                                                 ▼
                                      clinician_review  (interrupt / resume)
                                                 ▼
                                      finalise + audit log

    FastAPI exposes the workflow; a Streamlit screen is used for clinician review.

## 2. LangGraph state and nodes
**State (shared between nodes):** patient record, retrieved chunks with scores, safety flags,
draft options, validation errors, retry count, clinician decision, audit metadata.

| Node | Type | Responsibility |
|------|------|----------------|
| load_patient | Code | Fetch conditions, medicines, labs, allergies; detect out-of-scope populations |
| retrieve_guidelines | LangChain retriever | Hybrid search (vector + keyword) over protocol sections |
| evidence check | Conditional edge | Abstain if top relevance below threshold or out-of-scope population |
| check_drug_safety | Code | Kidney-function rules, allergy checks, openFDA label matches → flags |
| draft_options | LLM (Gemini) | 1-3 options with rationale, citations, flags; Pydantic schema |
| validate | Code | Citations exist, no dosing language, required flags present |
| clinician_review | Interrupt | Pause; resume with accept / edit / reject |
| finalise | Code | Store result and audit record |

## 3. Components
| Component | Technology |
|-----------|------------|
| Configuration | `src/copilot/config.py` (environment variables) |
| LLM and embeddings | Gemini via `langchain-google-genai` (provider-agnostic) |
| RAG | LangChain loaders, text splitters, retrievers |
| Vector store | PostgreSQL 16 + pgvector via `langchain-postgres` |
| Workflow | LangGraph with Postgres checkpointer |
| Clinical data | PostgreSQL tables loaded from Synthea FHIR |
| Drug safety | openFDA label API, RxNorm name normalisation, Python rules |
| API / UI | FastAPI; Streamlit review screen |
| Orchestration | Apache Airflow (nightly label refresh, batch evaluation) |
| Evaluation | pytest + scenario-based evaluation scripts |
| CI/CD | GitHub Actions (lint, tests, evaluation quality gate) |

## 4. Data model (initial)
- Vector store collection `protocols` (managed by langchain-postgres): chunk text, embedding, metadata (doc, section).
- `patients`, `conditions`, `medications`, `observations`, `allergies` (synthetic).
- `drug_labels(drug, rxcui, contraindications, drug_interactions, set_id, retrieved_at)`.
- `runs(run_id, patient_id, status, draft_json, model, prompt_version, created_at)`.
- `clinician_decisions(run_id, decision, clinician, comment, decided_at)`.
- `audit_log(run_id, node, model, tokens_in, tokens_out, latency_ms, chunk_ids, created_at)`.

## 5. Environments
| Environment | Where | Database | Secrets |
|-------------|-------|----------|---------|
| Development | GitHub Codespaces | pgvector in Docker | Codespaces secret |
| Production | Azure | Azure Database for PostgreSQL + pgvector | Azure Key Vault |

## 6. Security and privacy
- No secrets in code or Git.
- Patient identifiers redacted from logs and from LLM prompts where not needed.
- Read-only database role for retrieval and safety tools.
- Every run audited; outputs never final without clinician review.
