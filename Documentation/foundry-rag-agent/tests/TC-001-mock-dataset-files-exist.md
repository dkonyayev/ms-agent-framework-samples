---
id: TC-001
plan: ../plan.md
tasks: [T-002]
status: Current
last-synced: 2026-09-14
---

## Scope

Verify the mock fictional-company knowledge base (plan.md §4A.2) exists on disk
as a set of non-empty files, ready to be uploaded to Blob Storage in T-005.

## Preconditions

None (no Azure resources required — this checks local repo files only).

## Steps

1. List files under `data/mock-kb/`.
2. Confirm each file is non-empty.
3. Confirm the set of files spans all three topics required by §4A.2: product
   documentation, HR policy, and support FAQs.

## Expected result

At least one non-empty file exists for each of the three topics. As built:

- Product docs: `product-overview.md`, `product-pricing-plans.md`
- HR policy: `hr-policy-remote-work.md`, `hr-policy-pto.md`
- Support FAQs: `support-faq-billing.md`, `support-faq-troubleshooting.md`

## Result log

| Date | Who | Result | Actual |
|------|-----|--------|--------|
| 2026-09-14 | AI | ✅ Pass | 6 files present under `data/mock-kb/`, each 24–28 lines, covering all three required topics. |
