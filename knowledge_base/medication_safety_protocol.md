# Liffey Clinic Protocol: Medication Safety Checks

> Fictional protocol for a portfolio project. Not clinical guidance.

## MED-1 Allergies
Never suggest a medicine from a class to which the person has a recorded allergy. Flag the allergy for clinician review.

## MED-2 Interaction checks
Flag the following combinations for clinician review:
- ACE inhibitor or ARB with a potassium-sparing diuretic or potassium supplement: risk of high potassium.
- ACE inhibitor or ARB with a diuretic and an NSAID: increased risk of acute kidney injury.
- ACE inhibitor with ARB: see HTN-4.
- Any other interaction listed in the drug's product information.

## MED-3 Out-of-scope populations
Do not generate treatment options for people under 18, or who are pregnant or breastfeeding. State that the case is out of scope and refer to the specialist team.

## MED-4 Assistant behaviour
The assistant provides decision support for clinicians only. It must not give doses, titration schedules or administration instructions, must not address patients directly, and must cite the protocol section for every statement. Safety flags must ask the clinician to verify; the assistant never states that a medicine or combination is safe.