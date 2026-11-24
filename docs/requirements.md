# Requirements: Liffey Bank AML Investigation Copilot

**Status:** Draft v0.1  **Owner:** Pramod Makwana  **Date:** 2026-11-25

> Liffey Bank is fictional. All customer and transaction data is synthetic.

## 1. Problem statement
Transaction-monitoring systems generate large volumes of AML alerts, and most are false positives.
Analysts spend much of each investigation gathering facts (customer profile, KYC status,
transaction history, prior alerts) and looking up the relevant policy before they can make a decision.
This slows investigations and makes case documentation inconsistent.

## 2. Objectives
| ID | Objective | Measure (target, to be confirmed by evaluation) |
|----|-----------|-------------------------------------------------|
| OBJ-1 | Reduce time spent gathering facts per alert | Draft case file produced in under 60 seconds |
| OBJ-2 | Ground every statement in evidence or policy | 100% of claims linked to a transaction ID or policy section |
| OBJ-3 | Keep decisions with humans | 0 alerts closed or escalated without analyst approval |
| OBJ-4 | Protect personal data | 0 PII leaks in the safety test suite |

## 3. Scope
**In scope:** AML policy question answering with citations; alert investigation using customer,
account, transaction and alert data; a structured draft case file; analyst approve/reject;
an audit log; nightly batch investigation of new alerts.

**Out of scope:** automatic alert closure or SAR filing; real customer data; sanctions screening;
real-time (streaming) monitoring.

## 4. Stakeholders and users
| Role | Interest |
|------|----------|
| AML analyst (primary user) | Faster, consistent investigations |
| MLRO / compliance manager | Quality and consistency of decisions, regulatory defensibility |
| Internal audit / regulator | Traceability of every decision |
| IT / data engineering | Reliable, secure, maintainable service |

## 5. User stories
| ID | Story | Priority |
|----|-------|----------|
| US-01 | As an analyst, I want to ask a policy question and get an answer with the section cited, so I can apply policy correctly. | Must |
| US-02 | As an analyst, I want a draft case file for an alert, with customer profile, relevant transactions and matched typologies, so I start from evidence instead of a blank page. | Must |
| US-03 | As an analyst, I want to approve, edit or reject the draft, so the final decision is mine. | Must |
| US-04 | As an MLRO, I want every case file to record its inputs, model version and analyst decision, so decisions are auditable. | Must |
| US-05 | As an analyst, I want the copilot to say "insufficient evidence" instead of guessing. | Must |
| US-06 | As a compliance manager, I want new alerts investigated overnight, so drafts are ready each morning. | Should |
| US-07 | As an analyst, I want a draft SAR narrative for escalated cases. | Could |

## 6. Functional requirements
| ID | Requirement |
|----|-------------|
| FR-01 | Ingest policy documents, split them into sections/chunks, embed them, and store them in a vector store. |
| FR-02 | Answer policy questions using only retrieved policy text, with section citations. |
| FR-03 | Abstain when the retrieved policy text does not support an answer. |
| FR-04 | Investigate an alert by calling tools: customer profile, accounts, transactions, alert history, policy search. |
| FR-05 | Produce a case file in a defined JSON schema (summary, evidence, typologies, policy citations, suggested next step, confidence). |
| FR-06 | Record analyst decision (approve / edit / reject) with timestamp and user. |
| FR-07 | Write an audit record for every LLM call (prompt version, model, tokens, latency, retrieved chunk IDs). |
| FR-08 | Expose the service via an API (`/ask`, `/investigate/{alert_id}`, `/health`). |

## 7. Non-functional requirements
| ID | Category | Requirement |
|----|----------|-------------|
| NFR-01 | Security | No secrets in code; secrets from Codespaces secrets / Azure Key Vault. |
| NFR-02 | Privacy | Mask PII (names, IBANs, phone numbers, emails) before text is sent to the LLM. |
| NFR-03 | Resilience | Retry LLM calls with exponential backoff; fall back to a secondary model. |
| NFR-04 | Performance | Policy answer under 10 s; case file under 60 s (targets). |
| NFR-05 | Cost | Track tokens and estimated cost per request. |
| NFR-06 | Reproducibility | Locked dependencies (uv.lock); database schema as code. |
| NFR-07 | Quality | AI evaluation suite runs in CI; a drop in quality blocks the merge. |

## 8. Constraints and assumptions
- Free tiers only (Gemini API, GitHub Codespaces, Azure free account).
- Nothing stored on the developer's laptop; development happens in GitHub Codespaces.
- Synthetic data; policy documents are written for this project and are not real bank policy.
- The copilot supports analysts; it never makes the final decision.

## 9. Acceptance criteria (v1.0)
- Policy Q&A: at least 90% of evaluation questions answered correctly with the correct section cited.
- Investigation: case files for planted typologies identify the correct typology in at least 85% of cases.
- Safety: 100% of prompt-injection and PII-extraction tests refused.
- All tests and the evaluation suite pass in CI.

## 10. Risks
| Risk | Mitigation |
|------|------------|
| LLM hallucination | Retrieval-only answers, citation validation, abstain rule, evaluation |
| Provider outage / rate limits | Retries, backoff, fallback model |
| PII exposure | Masking before LLM calls, safety tests |
| Free-tier expiry | Code in GitHub, regenerable synthetic data, recorded demo |
| Evaluation bias (testing on the rules it was built from) | Held-out test cases written separately from the policy documents |
