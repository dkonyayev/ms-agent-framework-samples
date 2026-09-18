---
id: R-002
plan: ../plan.md
tasks: [T-004, T-005]
status: Current
last-verified: 2026-09-15
last-synced: 2026-09-15
---

## Goal

Deploy an embedding model in the Foundry project, and upload the mock dataset
to a dedicated Blob Storage container. This is prerequisite plumbing for R-003,
which builds the actual index via the native Knowledge Source flow.

## Prerequisites

See plan.md → Part 3. Also requires:
- `srch-kove-sandbox` provisioned (T-003, done).
- Mock dataset present at `data/mock-kb/` (T-002, done — 6 files, see §4A.2).

## Steps

### Part A — Deploy the embedding model (T-004)

1. In the Azure Portal, open the `ai-kove-foundry-sandbox` resource (or the
   Foundry project `proj-default` in the Azure AI Foundry portal).
2. Go to **Deployments → Deploy model**.
3. Select model **`text-embedding-3-small`**.
4. Deployment name: `text-embedding-3-small` (keep default unless it collides).
5. Deploy and wait for status **Succeeded**.

### Part B — Upload mock dataset to Blob Storage (T-005, step 1)

Use a **new, dedicated storage account** rather than the existing
`rgkovesandbox9653` — that one backs the `func-kove-sandbox` Function App, and
we don't want to touch its permissions or risk affecting it (see D-008).

1. In the Azure Portal, go to **Create a resource → Storage account**.
2. Fill in:
   - **Subscription:** Kove Enterprises Inc
   - **Resource group:** `rg-kove-sandbox`
   - **Storage account name:** `stmeridiankb` (must be globally unique,
     lowercase letters/numbers only, 3–24 chars — if taken, try
     `stmeridiankb01`, etc., and record the actual name used)
   - **Region:** `centralus`
   - **Performance:** Standard
   - **Redundancy:** Locally-redundant storage (LRS) — sufficient for this
     learning project
3. Review + create, wait for **Succeeded**.
4. Open the new storage account → **Containers → + Container**, name it
   `meridian-kb`, access level Private.
5. Upload all 6 files from `data/mock-kb/` into this container. If you hit the
   same "not authorized... Microsoft Entra ID" error here, it's because you're
   the account creator and should already have the Owner/Contributor role from
   creating it — if it still fails, switch the upload method in the container's
   toolbar from "Microsoft Entra User Account" to **"Access Key"** (shared key
   access is enabled by default on new storage accounts).

## Verify

- Portal → the new storage account → `meridian-kb` container shows all 6 files
  from `data/mock-kb/`.
- Portal → `ai-kove-foundry-sandbox` → Deployments shows `text-embedding-3-small`
  with status **Succeeded**.

## Rollback

Delete the `meridian-kb` container's blobs, or delete the storage account
entirely (it's dedicated to this project — see D-008). Delete the embedding
deployment from **Deployments** if no longer needed.

## Hand back

Paste into chat: the deployment name actually used for the embedding model (if
different from `text-embedding-3-small`), and the storage account name
actually used (if different from `stmeridiankb`). This closes T-004 and T-005
and fills plan.md §4A.3.

## Notes

- Integrated vectorization means Azure AI Search calls the embedding deployment
  itself during indexing (and again at query time) — no embedding code needs to
  be written in Python for this step.
- The actual index build now happens in **R-003**, via the native Knowledge
  Source flow (Agentic retrieval → Knowledge sources → Add knowledge source →
  Azure blob (Indexed)) rather than the classic Import-data wizard — see
  plan.md D-010/D-011.
