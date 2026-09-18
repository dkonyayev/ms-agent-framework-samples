---
id: R-001
plan: ../plan.md
tasks: [T-003]
status: Current
last-verified: 2026-09-14
last-synced: 2026-09-14
---

## Goal

Create the Azure AI Search service that will host the index, knowledge source,
and knowledge agent for this project.

## Prerequisites

See plan.md → Part 3 (subscription, resource group/region, Portal access).

## Steps

1. In the Azure Portal, go to **Create a resource → AI + Machine Learning → Azure AI Search**.
2. Fill in:
   - **Subscription:** Kove Enterprises Inc
   - **Resource group:** `rg-kove-sandbox`
   - **Service name:** `srch-kove-sandbox`
   - **Location:** `centralus`
   - **Pricing tier:** `Basic`
3. Click **Review + create**, then **Create**.
4. Wait for deployment to finish.

## Verify

- Portal resource overview shows provisioning state **Succeeded**.
- Optional: `az resource show --name srch-kove-sandbox --resource-group rg-kove-sandbox --resource-type Microsoft.Search/searchServices` returns the resource with `"provisioningState": "Succeeded"`.

## Cost note

Basic tier runs ~$75/mo while it exists (billed hourly, not per query). Free tier
was considered to avoid this but rejected — it does not support semantic ranker,
which agentic retrieval depends on for query planning/reranking (see plan.md D-006).
To avoid ongoing cost after this learning project, delete the service (see Rollback)
when you're done rather than leaving it running.

## Rollback

Delete the Azure AI Search resource from the Portal (Resource groups → `rg-kove-sandbox` → select the service → Delete). No other resources depend on it yet at this stage.

## Hand back

Once created, paste into chat: the provisioning state shown in the Portal (should be Succeeded). This closes T-003.

## Notes

- Tier must be Basic or above — semantic ranker (required for agentic retrieval's query planning/reranking) is not available on the Free tier.
- Region is centralus, not eastus (the Foundry resource's region) — eastus is blocked for this subscription (D-006). Cross-region use is fine; there's no hard requirement that Search and the Foundry/OpenAI resource share a region.
