---
id: TC-004
plan: ../plan.md
tasks: [T-008, T-009]
status: Current
last-synced: 2026-09-17
---

## Scope

End-to-end verification: the Foundry agent (`agent_with_agentic_rag.py`), using
`search_meridian_knowledge_base` as a tool, answers a question grounded in the
mock dataset via Azure AI Search agentic retrieval — not the Portal test panel
from TC-003, but the actual Python integration (§4A.7).

## Preconditions

- T-006/T-007 done (Knowledge Source + Knowledge Base live).
- `tools/knowledge_base_search.py` and `agent_with_agentic_rag.py` implemented.
- Local `.env` has `SEARCH_ENDPOINT`, `KNOWLEDGE_BASE_NAME`,
  `KNOWLEDGE_SOURCE_NAME`, and `SEARCH_API_KEY` set (see D-013 — AAD auth via
  `AzureCliCredential` returns 403 on this preview endpoint even for an Owner
  role; an admin API key is required for now).

## Steps

1. Run `py agent_with_agentic_rag.py`.
2. Observe the agent's printed answer to "How many PTO days do new hires get?"

## Expected result

A correct, grounded answer (20 days/year for full-time employees, front-loaded
January 1st, no waiting period for new hires) with a citation to the
`hr-policy-pto.md` blob.

## Result log

| Date | Who | Result | Actual |
|------|-----|--------|--------|
| 2026-09-17 | Human | ✅ Pass | Agent correctly answered with the prorated/no-waiting-period PTO policy and cited `https://stmeridiankb01.blob.core.windows.net/meridian-kb/hr-policy-pto.md`. |
