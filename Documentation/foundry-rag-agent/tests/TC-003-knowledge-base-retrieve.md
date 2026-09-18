---
id: TC-003
plan: ../plan.md
tasks: [T-007]
status: Current
last-synced: 2026-09-15
---

## Scope

Verify the Knowledge Base (`meridian-kb-agent`) returns a correct, grounded,
cited answer using the portal's built-in test/chat playground — before any
Python integration exists.

## Preconditions

- Knowledge Source `meridian-kb-source` finished creating (not stuck on
  "Creating").
- Knowledge Base `meridian-kb-agent` saved successfully, referencing
  `meridian-kb-source` and the `gpt-4o` chat completion model.

## Steps

1. Open the Knowledge Base's built-in test/chat panel in the Portal.
2. Ask: "How many PTO days do new hires get?"
3. Confirm the answer is grounded in `data/mock-kb/hr-policy-pto.md` and cites
   its source.

## Expected result

Answer states 20 days/year for full-time employees, prorated for new hires
based on start date, with no waiting period to begin using it — with a
citation to `hr-policy-pto.md` via `meridian-kb-source`.

## Result log

| Date | Who | Result | Actual |
|------|-----|--------|--------|
| 2026-09-15 | Human | ✅ Pass | Portal chat returned the correct prorated-PTO, no-waiting-period answer, cited `hr-policy-pto.md` / `meridian-kb-source`. |
