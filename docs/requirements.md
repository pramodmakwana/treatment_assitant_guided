# Requirements: Treatment Guideline Assistant

**Status:** Draft v0.2  **Owner:** Pramod Makwana  **Date:** 2026-11-25

> Decision-support prototype for portfolio purposes. All patients are synthetic (Synthea).
> Treatment protocols are fictional ("Liffey Clinic") and are not clinical guidance.
> This software is not a medical device and must not be used for real patient care.

## 1. Problem statement
Patients with several long-term conditions, such as type 2 diabetes, hypertension and chronic
kidney disease (CKD), need treatment that follows guidelines for each condition while accounting
for how the conditions and medicines interact. Kidney function, for example, changes which
medicines are appropriate. In a short appointment, a clinician must cross-check several
guidelines, the patient's current medicines and drug label warnings. This is time-consuming,
and contraindications or interactions can be missed.

## 2. Objectives
| ID | Objective | Measure (target, confirmed by evaluation) |
|----|-----------|-------------------------------------------|
| OBJ-1 | Give clinicians guideline-based treatment options quickly | Draft options in under 30 seconds |
| OBJ-2 | Ground every option in a cited protocol section | 100% of options cite a valid protocol section |
| OBJ-3 | Surface drug-safety concerns | At least 95% of planted contraindications flagged |
| OBJ-4 | Never produce unsafe output | 0 dosing instructions or patient-facing advice in safety tests |
| OBJ-5 | Keep the decision with the clinician | 0 outputs finalised without clinician review |

## 3. Scope
**In scope**
- Adult patients with type 2 diabetes, hypertension and/or CKD.
- Fictional Liffey Clinic treatment protocols as the knowledge base.
- Synthetic patient records (conditions, medicines, lab results such as HbA1c, eGFR, blood pressure).
- Drug-safety checks using openFDA drug labels (contraindications, drug interactions) and kidney-function rules.
- Draft treatment options with citations and safety flags; clinician review; audit trail.

**Out of scope**
- Dosing or titration advice.
- Diagnosis.
- Patient-facing advice.
- Prescribing, ordering or writing to a clinical system.
- Real patient data.
- Children, pregnancy and breastfeeding (the system abstains and flags these).

## 4. Stakeholders and users
| Role | Interest |
|------|----------|
| GP / clinician (primary user) | Fast, guideline-concordant options with safety flags |
| Clinical pharmacist | Accuracy of drug-safety flags |
| Clinical governance / safety officer | Safe behaviour, auditability, clear limitations |
| Patient (indirect) | Safer, guideline-based care |
| IT / engineering | Reliable, secure, maintainable service |

## 5. User stories
| ID | Story | Priority |
|----|-------|----------|
| US-01 | As a clinician, I want guideline-based treatment options for a patient's conditions, each citing the protocol section, so I can verify them quickly. | Must |
| US-02 | As a clinician, I want each option checked against the patient's current medicines, kidney function and allergies, so I don't miss a contraindication. | Must |
| US-03 | As a clinician, I want the assistant to say when no protocol covers the case, instead of guessing. | Must |
| US-04 | As a clinician, I want to accept, edit or reject the draft, so the final decision is mine. | Must |
| US-05 | As a clinical pharmacist, I want every safety flag to show its source (protocol rule or drug label section). | Must |
| US-06 | As a governance officer, I want every recommendation to record its inputs, retrieved sources, model version and clinician decision. | Must |
| US-07 | As a clinician, I want to ask a free-text question about the protocols and get a cited answer. | Should |
| US-08 | As an administrator, I want drug label data refreshed automatically, so safety checks stay current. | Should |

## 6. Functional requirements
| ID | Requirement |
|----|-------------|
| FR-01 | Load protocol documents, split them by section, embed them and store them in pgvector (LangChain). |
| FR-02 | Load synthetic patient records: conditions, medicines, lab results, allergies. |
| FR-03 | Retrieve protocol sections relevant to the patient's conditions and lab values (hybrid: vector + keyword). |
| FR-04 | Abstain when retrieved evidence is insufficient (relevance below threshold). |
| FR-05 | Check candidate medicines against the patient's medicines, kidney function and allergies using deterministic rules and openFDA label sections. |
| FR-06 | Draft 1-3 treatment options as structured output: option, rationale, protocol citations, safety flags, confidence. |
| FR-07 | Validate the draft: citations exist, no dosing language, flags present where rules fired. Redraft at most twice on failure. |
| FR-08 | Pause for clinician review (LangGraph interrupt); resume on accept / edit / reject. |
| FR-09 | Persist workflow state (LangGraph Postgres checkpointer) so paused reviews survive restarts. |
| FR-10 | Write an audit record for every run: patient ID, retrieved chunk IDs, model, prompt version, tokens, latency, flags, clinician decision. |
| FR-11 | Expose an API: `/recommend/{patient_id}`, `/review/{run_id}`, `/ask`, `/health`. |
| FR-12 | Refresh drug label data on a schedule (Airflow). |

## 7. Safety requirements
| ID | Requirement |
|----|-------------|
| SR-01 | Never output doses, titration schedules or administration instructions. |
| SR-02 | Never address the patient directly; output is for clinicians only. |
| SR-03 | Every clinical statement must cite a protocol section or label section. |
| SR-04 | Abstain when no protocol covers the case or evidence is insufficient. |
| SR-05 | Safety flags say "verify"; the system never states that a medicine or combination is "safe". |
| SR-06 | Abstain and flag for out-of-scope populations: under 18, pregnancy, breastfeeding. |
| SR-07 | Redact patient identifiers from logs and from text sent to the LLM where not needed. |
| SR-08 | No output is final without clinician review. |
| SR-09 | Refuse prompt-injection attempts and requests outside clinical decision support. |

## 8. Non-functional requirements
| ID | Category | Requirement |
|----|----------|-------------|
| NFR-01 | Security | No secrets in code; Codespaces secrets in development, Azure Key Vault in production. |
| NFR-02 | Resilience | Retries with exponential backoff; fallback LLM model. |
| NFR-03 | Performance | Recommendation under 30 s; protocol Q&A under 10 s (targets). |
| NFR-04 | Cost | Tokens and estimated cost recorded per run. |
| NFR-05 | Portability | Provider-agnostic LLM layer via LangChain (Gemini by default). |
| NFR-06 | Reproducibility | Locked dependencies (uv.lock); infrastructure as code (docker-compose, schema). |
| NFR-07 | Quality | Evaluation and safety suites run in CI; a quality drop blocks the merge. |

## 9. Constraints and assumptions
- Free tiers only (Gemini API, GitHub Codespaces, Azure free account).
- Nothing stored on the developer's laptop; development in GitHub Codespaces.
- Gemini free tier may use prompts to improve Google products; acceptable only because all data is synthetic.
  A real deployment would use an enterprise endpoint with no training on customer data.
- openFDA labels are US labels; an Irish deployment would use EU product information (SmPC).

## 10. Acceptance criteria (v1.0)
- At least 90% of evaluation scenarios produce options that cite the correct protocol section.
- At least 95% of planted contraindications and interactions are flagged.
- 100% of safety tests pass (no dosing, no patient-facing advice, correct abstentions, injection refused).
- All tests and evaluation suites pass in CI.

## 11. Risks
| Risk | Mitigation |
|------|------------|
| Hallucinated recommendation | Retrieval-only drafting, citation validation, abstain rule, evaluation |
| Missed contraindication | Deterministic rules for known risks; label checks; "verify" flags; pharmacist review |
| Over-trust by users | Clear "decision support only" framing; mandatory clinician review |
| Provider outage / rate limits | Retries, backoff, fallback model |
| Circular evaluation | Test scenarios written separately from protocol text; held-out set |
| Free-tier expiry | Code in GitHub; regenerable synthetic data; recorded demo |

## 12. Regulatory considerations
- **EU MDR:** software intended to inform treatment decisions may qualify as a medical device.
  This prototype is not CE-marked and is for demonstration only.
- **EU AI Act:** AI that is, or is part of, a medical device is generally treated as high-risk,
  requiring risk management, data governance, human oversight, logging and transparency.
  The design mirrors these practices (human review, audit log, documented limitations).
- **GDPR:** health data is special-category personal data; real use would need a lawful basis,
  data minimisation and a DPIA. This project uses only synthetic data.
