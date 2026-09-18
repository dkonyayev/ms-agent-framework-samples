---
id: R-003
plan: ../plan.md
tasks: [T-006, T-007]
status: Current
last-verified: 2026-09-15
last-synced: 2026-09-15
---

## Goal

Create the Knowledge Source (which ingests, vectorizes, and indexes the mock
dataset in one step) and the Knowledge Base (knowledge agent) that references
it — using this portal's native Agentic retrieval flow rather than the classic
Import-data wizard (see plan.md D-010/D-011).

## Prerequisites

See plan.md → Part 3. Also requires:
- `text-embedding-3-small` deployed (T-004, R-002 Part A).
- Mock dataset uploaded to `stmeridiankb` / `meridian-kb` container (T-005, R-002 Part B).

## Steps

### Part A0 — Enable Managed Identity for the Search service (once, before T-006)

The vectorizer needs to call the `text-embedding-3-small` deployment. Use
Managed Identity rather than an API key, to match this repo's no-secrets-in-
config pattern (see D-012).

1. Open `srch-kove-sandbox` → **Settings → Identity**.
2. Under **System assigned**, set **Status** to **On**, Save.
3. Open `ai-kove-foundry-sandbox` → **Access control (IAM) → Add → Add role
   assignment**.
4. Role: **Cognitive Services OpenAI User**. Assign access to: **Managed
   identity → Search service → `srch-kove-sandbox`**. Save.

### Part A — Create the Knowledge Source (T-006)

1. Open `srch-kove-sandbox` → left nav **Agentic retrieval → Knowledge sources**.
2. Click **Add knowledge source → Azure blob (Indexed)**.
3. Fill in:
   - **Name:** `meridian-kb-source`
   - **Description:** "Meridian Cloudworks mock knowledge base (product docs, HR policy, support FAQs)"
   - **Subscription:** Kove Enterprises Inc
   - **Storage account:** `stmeridiankb`
   - **Blob container:** `meridian-kb`
   - **Blob folder:** leave blank
   - **Content extraction → Mode:** Minimal
   - Leave "Enable sensitivity labels" and "Authenticate using managed identity" unchecked
4. Under **Enable text vectorization**, click **Add vectorizer** and select the
   Azure OpenAI resource `ai-kove-foundry-sandbox` with deployment
   `text-embedding-3-small`. Authentication: **Managed Identity** (requires
   Part A0 done first) rather than API Key.
5. Leave **Enable image verbalization** off — no images in the mock dataset, so
   skip "Add chat completion model" / "Add asset store" here.
6. Leave **Advanced configurations** at defaults unless noted otherwise after
   review.
7. Create, and wait for the underlying index/indexer to finish building (the
   knowledge source list will show it once ready).

### Part B — Create the Knowledge Base (T-007)

1. Left nav **Agentic retrieval → Knowledge bases → Add knowledge base**.
2. **Basics:**
   - **Name:** `meridian-kb-agent`
   - **Description:** (optional) "Knowledge base over the Meridian Cloudworks mock docs"
   - **Knowledge sources:** click **Add existing**, select `meridian-kb-source`
     (it may still show status "Creating" from Part A — wait for it to finish
     before proceeding)
3. **Retrieval:**
   - **Reasoning effort:** `Low` (cheapest/simplest for this learning project;
     Medium/High spend more on query planning — revisit later if answers are
     weak)
   - **Retrieval instructions:** (optional but useful) e.g. "Answer questions
     about Meridian Cloudworks' product, HR policy, and support documentation,
     grounded only in the provided knowledge source."
   - **Chat completion model:** click **Add model deployment** and select the
     `gpt-4o` deployment — this is required (the form will block Save without
     it, since a model deployment is mandatory even at reasoning effort Low).
4. Leave **Output configurations** and **Encryption** at their defaults
   (expand only if you want to review them).
5. Click **Save**, and wait for status to move from "Creating" to ready.

## Verify

- **Knowledge sources** page lists `meridian-kb-source` with no errors.
- Portal → Indexes shows a new index (auto-named by the knowledge source) with
  **Document Count: 6** or more (chunked).
- **Knowledge bases** page lists `meridian-kb-agent` referencing
  `meridian-kb-source`.
- If the portal offers a built-in chat/test playground for the knowledge base,
  ask it a question grounded in the mock data (e.g. "How many PTO days do new
  hires get?") and confirm it returns the correct, cited answer (20 days,
  front-loaded, from `hr-policy-pto.md`) — this doubles as an early look at
  TC-003/TC-004.

## Rollback

Delete the Knowledge Base first (Part B), then the Knowledge Source (Part A) —
deleting the source before the base may error since the base references it.
Deleting the Knowledge Source also removes its auto-created index/indexer.

## Hand back

Paste into chat: the actual Knowledge Source name (if different), the
auto-created index name, the reasoning effort level actually used, and the
document count shown. This closes T-006/T-007 and fills plan.md
§4A.4/§4A.5/§4A.6.

## Notes

- This flow supersedes the earlier plan to use "Import data → RAG" (R-002's
  old Part C) — the Knowledge Source's own ingestion pipeline builds the index,
  so there's no separate manual index-build step (see D-010/D-011).
- "Knowledge base" here is this portal's display name for what the Search REST
  API and SDK call a **knowledge agent** — §4A.7's Python integration will use
  the `knowledge agent` / `retrieve` terminology from the API.
- **Why the Knowledge Base needs its own chat completion model, separate from
  the Foundry agent's model:** the Foundry agent's model (`gpt-4o` in
  `agent_simple.py`/`foundry_client.py`) drives the overall conversation —
  deciding when to call tools and composing the final reply to the user. The
  Knowledge Base's chat completion model runs *inside Azure AI Search itself*,
  as part of agentic retrieval's own pipeline: it breaks the query into
  sub-queries, picks which knowledge sources to search, and (depending on
  reasoning effort) synthesizes/reranks retrieved chunks before handing
  results back to whatever calls it. That's what makes retrieval "agentic"
  rather than a single vector search — Search needs its own LLM to do that
  planning, independent of any particular caller. Both happen to point at the
  same `gpt-4o` deployment here, but they're conceptually separate: a
  Knowledge Base could be called by multiple different agents, each with a
  different model of their own.
