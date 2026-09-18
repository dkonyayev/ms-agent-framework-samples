---
id: TC-002
plan: ../plan.md
tasks: [T-006]
status: Current
last-synced: 2026-09-15
---

## Scope

Verify the index auto-created by the Knowledge Source (`meridian-kb-source`)
is actually populated with the mock dataset.

## Preconditions

- Knowledge Source `meridian-kb-source` finished creating (not "Creating").

## Steps

1. Portal → `srch-kove-sandbox` → Indexes → find the index auto-created by
   `meridian-kb-source`.
2. Confirm document count > 0 (expect 6, or more if chunked per-document).
3. Confirm the indexer's last run shows 0 failed documents.

## Expected result

Index shows a non-zero document count with no failed documents.

## Result log

| Date | Who | Result | Actual |
|------|-----|--------|--------|
| 2026-09-15 | Human | ✅ Pass (inferred) | Not checked directly via the Indexes tab, but TC-003's grounded, correctly-cited retrieval from `hr-policy-pto.md` confirms the index is populated and queryable. Exact index name/doc count still to be recorded in plan.md §4A.4 — paste them in when convenient. |
