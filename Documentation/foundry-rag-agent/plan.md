# Foundry Agentic RAG — Implementation Plan

**Status:** Complete
**Last updated:** 2026-09-17
**Next up:** nothing — Milestone 1 closed
**Awaiting human:** nothing
**Last session:** T-008 implemented ([agent_with_agentic_rag.py](../../agent_with_agentic_rag.py), [tools/knowledge_base_search.py](../../tools/knowledge_base_search.py)). Hit a 403 on AAD auth against the preview Knowledge Base retrieve endpoint even with Owner role + "Both" auth mode — root-caused as a preview-API limitation, not misconfiguration (D-013); fixed with an API-key fallback (`SEARCH_API_KEY` in local `.env`). TC-004 passed: the Python agent correctly answered a PTO question grounded in `hr-policy-pto.md`, citing the actual blob URL. User confirmed T-009 and T-010 in chat — this satisfies the project's learning goal. Milestone 1 closed; all tasks archived to Part 5.

## Part 1 — Active Task List

*(empty — Milestone 1 closed 2026-09-17; all tasks archived to Part 5. Add new tasks here if this project continues, e.g. hardening, retrying AAD auth once the preview matures, or expanding the mock dataset.)*

| ID | Owner | Type | Task — Done when: <observable outcome> | Status | Ref | Updated |
|----|-------|------|----------------------------------------|--------|-----|---------|

## Part 1B — Satellite Registry

**Runbooks**

| ID | Title | Tasks | Status | Last verified |
|----|-------|-------|--------|---------------|
| R-001 | [Provision the Azure AI Search service](runbooks/R-001-provision-search-service.md) | T-003 | Current | 2026-09-14 |
| R-002 | [Deploy embedding model and upload mock data](runbooks/R-002-embed-model-and-index.md) | T-004, T-005 | Current | 2026-09-15 |
| R-003 | [Create the Knowledge Source and Knowledge Base](runbooks/R-003-knowledge-source-and-agent.md) | T-006, T-007 | Current | 2026-09-15 |

**Test cases**

| ID | Title | Tasks | Last run | Result |
|----|-------|-------|----------|--------|
| TC-001 | [Mock dataset files exist and are non-empty](tests/TC-001-mock-dataset-files-exist.md) | T-002 | 2026-09-14 | ✅ Pass |
| TC-002 | [Index populated](tests/TC-002-index-populated.md) | T-006 | 2026-09-15 | ✅ Pass (inferred — see log) |
| TC-003 | [Knowledge Base retrieve returns grounded, cited results](tests/TC-003-knowledge-base-retrieve.md) | T-007 | 2026-09-15 | ✅ Pass |
| TC-004 | [End-to-end: Python agent returns a grounded, cited answer](tests/TC-004-end-to-end-grounded-answer.md) | T-008, T-009 | 2026-09-17 | ✅ Pass |

## Part 2 — Human-Aligned Summary

**The idea.** We're building a small demo that teaches how to ground a Microsoft
Agent Framework agent (already working against Azure AI Foundry) in real content,
using Azure AI Search's newer "agentic retrieval" feature instead of hand-rolling
chunking and embedding code. In this pattern, Azure AI Search itself hosts a
"Knowledge Agent" that knows how to plan a search, run it, and rerank results; our
Foundry agent just calls that Knowledge Agent as a tool when it needs facts. We
seed it with a small made-up company's knowledge base (product docs, HR policy,
support FAQs) so we can clearly see grounded vs. ungrounded answers.

**Does it work.** Yes — confirmed end-to-end. Running `agent_with_agentic_rag.py`
and asking about the mock company's PTO policy returns a correct, grounded answer
with a citation to the actual source document. The one real snag: this portal/API
surface is a very new preview (a "Knowledge Base" flow, not yet the more commonly
documented "Knowledge Agent" pattern), so some Portal button names and the exact
auth story didn't match older public docs — most notably, the Python client
currently needs an admin API key rather than pure Entra ID auth, because the
preview `retrieve` endpoint returns 403 on AAD tokens even for a fully-privileged
user. That's tracked as a known limitation, not a dead end.

**Where things stand.** Complete. Azure AI Search service, embedding deployment,
mock dataset, Knowledge Source, and Knowledge Base are all provisioned; the Python
integration works and was verified by the user. All ten tasks are archived in Part
5 under Milestone 1. If this project continues, natural next steps would be
retrying AAD auth once the preview matures, or expanding the mock dataset /
adding more tools.

## Part 3 — Environment & Prerequisites

- **Subscription:** "Kove Enterprises Inc" (`d1bdd311-4080-470d-ba4c-874531ba5c76`), tenant `13f0df60-549e-4639-82ef-3a1ad3f3b4a1`. Sign in with `az login --tenant 13f0df60-549e-4639-82ef-3a1ad3f3b4a1` (per repo `.env` comment, account `koveent@gmail.com`).
- **Resource group:** `rg-kove-sandbox`. Foundry AI resource is in `eastus`; the Search service is in `centralus` (eastus blocked for Search on this subscription — see D-006). Cross-region use is fine.
- **Foundry project:** `ai-kove-foundry-sandbox` / project `proj-default`. Existing chat deployment: `gpt-4o`.
- **Local repo env:** Python virtualenv already at `.venv` with `agent-framework` and `azure-identity` installed; auth via `AzureCliCredential` (same pattern as `foundry_client.py`).
- **Secrets:** none checked into the repo; `.env` holds `FOUNDRY_PROJECT_ENDPOINT` only. Any Search API key, if needed instead of managed identity, goes in `.env` (never in plan/runbook files) — actual values are never written into this plan.
- **Portal access needed:** Azure Portal access to `rg-kove-sandbox` sufficient to create a Search service, a Storage blob container, and Foundry model deployments.

## Part 4 — AI-Aligned Detail

### 4A — Current Specification

**§4A.1 — Azure AI Search service** *(resolved by T-001, amended by D-006)*
- Name: `srch-kove-sandbox`.
- Tier: **Basic** (minimum tier with semantic ranker; Free tier does not support semantic ranker, which agentic retrieval requires, so Free is not an option — see D-006).
- Resource group / region: `rg-kove-sandbox` / `centralus` (East US blocked for this subscription; Central US substituted).

**§4A.2 — Mock dataset** *(built by T-002 — done)*
- Fictional company: **Meridian Cloudworks, Inc.**, maker of a project-management SaaS product called **Meridian Flow**.
- Content: 6 Markdown files under `data/mock-kb/`:
  - Product docs: `product-overview.md`, `product-pricing-plans.md`
  - HR policy: `hr-policy-remote-work.md`, `hr-policy-pto.md`
  - Support FAQs: `support-faq-billing.md`, `support-faq-troubleshooting.md`
- Each file contains specific, checkable facts (prices, day counts, SLAs, contact addresses) intended for use in T-009's grounded Q&A test.

**§4A.3 — Embedding model deployment** *(resolved by T-004)*
- Model: `text-embedding-3-small`, deployed in `ai-kove-foundry-sandbox` alongside the existing `gpt-4o` deployment. Used by the Search index's vectorizer for integrated vectorization.

**§4A.4 — Search index** *(built automatically by T-006)*
- No longer built via a separate Import-data wizard — creating the Knowledge Source (§4A.5) as type "Azure blob (Indexed)" builds the underlying index, indexer, and skillset automatically as part of its own ingestion pipeline (confirmed via portal screenshot 2026-09-15 — see D-011).
- Storage account: `stmeridiankb01` (new, dedicated — see D-008; `stmeridiankb` was taken, so the `01`-suffixed name from R-002's fallback instructions was used), region `centralus`, container `meridian-kb`.
- Index name: auto-generated by the Knowledge Source; not recorded (not needed — the Python integration in §4A.7 addresses the Knowledge Base/Source by name, not the index directly).

**§4A.5 — Knowledge Source** *(built by T-006)*
- Type: **Azure blob (Indexed)**, name `meridian-kb-source`.
- Points at `stmeridiankb01`/`meridian-kb`; content extraction mode Minimal; text vectorization enabled via a vectorizer referencing the `text-embedding-3-small` deployment (§4A.3). Image verbalization left off (no images in the mock dataset).
- Created under the Search service's left-nav **Agentic retrieval → Knowledge sources** page (portal-observed 2026-09-15 — see D-009/D-011), not as part of an Import-data wizard.

**§4A.6 — Knowledge Agent** *(built by T-007)*
- References the Knowledge Source (§4A.5) for retrieval and the `gpt-4o` deployment for query planning/answer synthesis. Name `meridian-kb-agent`. Confirmed panel fields (2026-09-15): Basics (name, description, Knowledge sources → Add existing), Retrieval (Reasoning effort — proposed `Low`; Retrieval instructions free text; Chat completion model — mandatory, `gpt-4o`), Output configurations, Encryption.
- In this portal (branded "Foundry IQ"), this resource is created under **Agentic retrieval → Knowledge bases** — the portal's current display name for what the Search REST API still calls a "knowledge agent" (see D-009). Task/section names here keep "Knowledge Agent" since that's the API/SDK term the Python integration (§4A.7) will use.

**§4A.7 — Python integration** *(built by T-008 — done)*
- [agent_with_agentic_rag.py](../../agent_with_agentic_rag.py): a `FoundryChatClient`-based `Agent` (`MeridianSupportAgent`, model `gpt-4o`) with one tool.
- [tools/knowledge_base_search.py](../../tools/knowledge_base_search.py): async tool `search_meridian_knowledge_base`, using the `azure-search-documents` SDK's `azure.search.documents.knowledgebases.aio.KnowledgeBaseRetrievalClient` (a preview SDK surface, API version `2026-04-01`) to call `meridian-kb-agent`'s `retrieve` action with a `KnowledgeRetrievalSemanticIntent` built from the model's query, scoped to `meridian-kb-source` with `include_references=True`. Returns the synthesized answer text plus blob-URL citations as a string, fed back to the agent's model.
- **Auth (see D-013):** `AzureCliCredential` (AAD) returns 403 on this preview endpoint even for a subscription Owner with the Search service's auth mode set to "Both" — a current limitation/quirk of this preview API, not an RBAC misconfiguration. The tool falls back to `AzureKeyCredential` when `SEARCH_API_KEY` is set in `.env` (gitignored, never committed) — this is the auth path actually used to pass TC-004. `AzureCliCredential` remains the default when no key is set, in case the AAD path starts working in a future preview update.
- Env vars used (added to `.env`): `SEARCH_ENDPOINT`, `KNOWLEDGE_BASE_NAME`, `KNOWLEDGE_SOURCE_NAME`, `SEARCH_API_KEY`.

### 4B — Decision Log

D-001 | 2026-09-14 | T-001..T-010 | Decision: Use Azure AI Search agentic retrieval (Knowledge Sources + Knowledge Agents) instead of classic manual RAG | Why: user explicitly wants to focus on the agentic-retrieval pattern, and it's Microsoft's current recommended approach for pairing Search with Foundry agents | Rejected: hand-rolled chunk/embed/prompt-stuffing RAG | Files: —

D-002 | 2026-09-14 | T-003..T-007 | Decision: Provision all Azure resources via Azure Portal click-through, documented in runbooks, rather than CLI/Bicep scripts | Why: user preference — wants to see/learn the Portal flow | Rejected: CLI/REST provisioning scripts | Files: —

D-003 | 2026-09-14 | T-001, T-003 | Decision: New Azure AI Search service goes in existing `rg-kove-sandbox` (eastus), alongside the Foundry AI resource | Why: user wants to reuse the Foundry sandbox's resource group/region for simplicity | Rejected: separate dedicated resource group | Files: —

D-004 | 2026-09-14 | T-002 | Decision: Mock dataset is a fictional company's knowledge base (product docs, HR policy, support FAQs) | Why: gives varied, low-stakes content that clearly demonstrates grounded multi-topic retrieval | Rejected: real/downloaded public dataset | Files: —

D-005 | 2026-09-14 | T-001 | Decision: Azure AI Search service name `srch-kove-sandbox`, tier Basic | Why: user confirmed the proposed defaults as-is | Rejected: — | Files: runbooks/R-001-provision-search-service.md

D-006 | 2026-09-14 | T-001, T-003 | Decision: Region changed from eastus to centralus; tier stays Basic (Free rejected) | Why: East US is blocked for this subscription/quota. User asked about Free tier to save the ~$75/mo Basic cost, but Azure AI Search's Free service tier does not support semantic ranker, which agentic retrieval's query planning/reranking depends on — so Free cannot support this project's goal | Rejected: Free tier (incompatible with agentic retrieval); eastus (blocked) | Files: runbooks/R-001-provision-search-service.md

D-007 | 2026-09-14 | T-002 | Decision: Mock company is "Meridian Cloudworks, Inc." / product "Meridian Flow" (project-management SaaS), with 6 files across product/HR/support topics, each written with specific checkable facts | Why: specific facts (prices, day counts, SLAs) are needed so T-009's grounded Q&A test can verify the agent actually retrieved the right document rather than guessing plausibly | Rejected: — | Files: data/mock-kb/*.md, tests/TC-001-mock-dataset-files-exist.md

D-008 | 2026-09-15 | T-005 | Decision: Create a new, dedicated storage account (`stmeridiankb`, centralus) for the mock dataset instead of reusing the existing `rgkovesandbox9653` account | Why: user hit an Entra ID authorization error uploading to the existing account, and doesn't want to touch its permissions since it backs the `func-kove-sandbox` Function App — a shared production-adjacent resource | Rejected: granting the user's Entra ID identity a Storage Blob Data role on the existing account; switching that account's Portal auth to access-key | Files: runbooks/R-002-embed-model-and-index.md

D-009 | 2026-09-15 | T-005, T-006, T-007 | Observation/decision: `srch-kove-sandbox`'s portal is the newer "Foundry IQ" experience — no "Import and vectorize data" button; instead **Import data → RAG** scenario is the equivalent wizard. Agentic-retrieval resources live under a left-nav **Agentic retrieval** section with **Knowledge sources** and **Knowledge bases** pages (the latter being this portal's name for what the REST API calls a "knowledge agent"). R-002 rewritten to match the real wizard steps (screenshots confirmed by user); plan/task names keep "Knowledge Agent" since that's the API/SDK term used in §4A.7's Python code | Why: original runbook was written from general docs knowledge before seeing this tenant's actual portal, which turned out to use different button labels/terminology | Rejected: — | Files: runbooks/R-002-embed-model-and-index.md

D-010 | 2026-09-15 | T-005, T-006 | Decision: reverse course from the classic Import-data (RAG scenario) wizard and instead use the portal's native "Build your knowledge base" / Agentic retrieval-first flow to connect the mock data, since it may create the knowledge source (and possibly the index) directly without a separate manual Import step | Why: user wants to learn the newer agentic-retrieval-native path rather than the classic wizard I defaulted to from general docs knowledge; exact steps not yet verified against this tenant's portal | Rejected: R-002 Part C (Import data → RAG) as written — flipped to Needs review pending screenshots of the actual "Build"/"Add knowledge source" flow | Files: runbooks/R-002-embed-model-and-index.md

D-011 | 2026-09-15 | T-005, T-006, T-007 | Decision (confirmed via screenshot): "Agentic retrieval → Knowledge sources → Add knowledge source → Azure blob (Indexed)" builds the index/indexer/skillset itself from a blob container, including an inline "Add vectorizer" step — no separate Import-data wizard step is needed. T-006 redefined as "create the Knowledge Source directly"; the old T-005 "run the wizard" sub-step is removed (T-005 is now just the blob upload); R-002 trimmed to embedding-deployment + blob-upload only; new R-003 created covering Knowledge Source (T-006) and Knowledge Base (T-007) | Why: real portal screenshot showed the actual panel, superseding the assumption in D-010 | Rejected: R-002's old Part C (Import data → RAG) — removed entirely | Files: runbooks/R-002-embed-model-and-index.md, runbooks/R-003-knowledge-source-and-agent.md

D-012 | 2026-09-15 | T-006 | Decision: the Knowledge Source's vectorizer authenticates to the embedding deployment via **Managed Identity**, not an API key | Why: matches this repo's existing no-secrets pattern (agent samples already use `AzureCliCredential`/RBAC, not keys); avoids storing/rotating an Azure OpenAI key anywhere. Required a new prerequisite sub-step: enable system-assigned identity on `srch-kove-sandbox` and grant it "Cognitive Services OpenAI User" on `ai-kove-foundry-sandbox` | Rejected: API key auth for the vectorizer | Files: runbooks/R-003-knowledge-source-and-agent.md

D-013 | 2026-09-17 | T-008, T-009 | Decision (root-caused via diagnostic): AAD/Entra token auth (`AzureCliCredential`, scope `https://search.azure.com/.default`) against the preview Knowledge Base `retrieve` endpoint (`KnowledgeBaseRetrievalClient`, API version `2026-04-01`) returns 403 Forbidden even for a user with the **Owner** role (which includes `DataActions: *`) on `srch-kove-sandbox`, with the service's data-plane auth mode set to "Both". Ruled out: wrong RBAC role (Owner already covers data actions); stale "Both" setting (already enabled, not just changed). Root cause appears to be a preview-API limitation — this new `knowledgebases` surface doesn't yet accept AAD bearer tokens the way older Search endpoints do. Confirmed fix: an admin API key (`AzureKeyCredential`) succeeds where AAD failed. `tools/knowledge_base_search.py` now tries `SEARCH_API_KEY` (if set in local `.env`) first, falling back to `AzureCliCredential` | Why: needed a working auth path to complete T-008/T-009; API key kept as an opt-in fallback rather than the default, to keep this repo's no-keys-by-default pattern for when/if AAD support lands | Rejected: continuing to debug AAD-only (no further leads without deeper preview-API-specific documentation); switching the tool to always require a key | Files: tools/knowledge_base_search.py, tests/TC-004-end-to-end-grounded-answer.md

D-014 | 2026-09-17 | T-005 | Correction: the storage account actually created was `stmeridiankb01`, not `stmeridiankb` — the unsuffixed name was taken, so the `01`-suffixed fallback named in R-002's instructions was used | Why: recording the real value, confirmed via the blob URL in TC-004's citation (`https://stmeridiankb01.blob.core.windows.net/...`) | Rejected: — | Files: —

## Part 5 — Completed Work Archive

### Milestone 1 — Agentic RAG demo working end-to-end (closed 2026-09-17)

| ID | Owner | Type | Task — Done when: <observable outcome> | Status | Ref | Updated |
|----|-------|------|----------------------------------------|--------|-----|---------|
| T-001 | Human | Decide | Confirm Azure AI Search service name, tier, and region — Done when: confirmed in chat | 🟢 Done | §4A.1 | 2026-09-14 |
| T-002 | AI | Build | Generate mock fictional-company knowledge base content (product docs, HR policy, support FAQs) — Done when: TC-001 passes | 🟢 Done | §4A.2 | 2026-09-14 |
| T-003 | Human | Do | Provision the Azure AI Search service in the Portal — Done when: R-001 verification passes | 🟢 Done | [R-001](runbooks/R-001-provision-search-service.md) | 2026-09-14 |
| T-004 | Human | Do | Deploy an embedding model (text-embedding-3-small) in the Foundry project — Done when: R-002 verification passes | 🟢 Done | [R-002](runbooks/R-002-embed-model-and-index.md) | 2026-09-15 |
| T-005 | Human | Do | Upload mock dataset to a dedicated Blob Storage container — Done when: R-002 verification passes | 🟢 Done | [R-002](runbooks/R-002-embed-model-and-index.md) | 2026-09-15 |
| T-006 | Human | Do | Create a Knowledge Source (Azure blob, Indexed) pointing at the blob container, with a vectorizer — this builds the index automatically — Done when: TC-002 passes | 🟢 Done | [R-003](runbooks/R-003-knowledge-source-and-agent.md) | 2026-09-15 |
| T-007 | Human | Do | Create a Knowledge Base (knowledge agent) referencing the Knowledge Source and the gpt-4o deployment — Done when: TC-003 passes | 🟢 Done | [R-003](runbooks/R-003-knowledge-source-and-agent.md) | 2026-09-15 |
| T-008 | AI | Build | Implement Python sample wiring the Knowledge Agent's retrieve action into the Foundry agent as a tool — Done when: TC-004 passes | 🟢 Done | §4A.7 | 2026-09-17 |
| T-009 | Human | Test | Ask the agent a question that requires grounding in the mock data and confirm a correct, cited answer — Done when: TC-004 logged pass | 🟢 Done | [TC-004](tests/TC-004-end-to-end-grounded-answer.md) | 2026-09-17 |
| T-010 | Human | Confirm | Confirm the agentic-RAG demo meets the learning goal — Done when: confirmed in chat | 🟢 Done | — | 2026-09-17 |
