# Tool wrapping Azure AI Search agentic retrieval (Knowledge Base) for the
# Meridian Cloudworks mock knowledge base. See Documentation/foundry-rag-agent/
# plan.md §4A.5-4A.7 for how the underlying Knowledge Source and Knowledge Base
# were provisioned.

import os
from contextlib import AsyncExitStack
from typing import Annotated

from agent_framework import tool
from azure.core.credentials import AzureKeyCredential
from azure.identity.aio import AzureCliCredential
from azure.search.documents.knowledgebases.aio import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    AzureBlobKnowledgeSourceParams,
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalSemanticIntent,
)
from pydantic import Field


@tool(approval_mode="never_require")
async def search_meridian_knowledge_base(
    query: Annotated[
        str,
        Field(description="A natural-language question about Meridian Cloudworks' product, pricing, HR policy, or support topics."),
    ],
) -> str:
    """Search the Meridian Cloudworks knowledge base (product docs, HR policy, support FAQs) and return a grounded, cited answer."""
    endpoint = os.environ["SEARCH_ENDPOINT"]
    knowledge_base_name = os.environ.get("KNOWLEDGE_BASE_NAME", "meridian-kb-agent")
    knowledge_source_name = os.environ.get("KNOWLEDGE_SOURCE_NAME", "meridian-kb-source")

    # DIAGNOSTIC (temporary): AAD auth via AzureCliCredential returns 403 on
    # this preview knowledge-base retrieve endpoint despite Owner role + "Both"
    # auth mode on the Search service. If SEARCH_API_KEY is set locally, use an
    # API key instead to isolate whether this preview endpoint currently
    # requires it. Remove this fallback once root-caused (see plan.md T-008).
    api_key = os.environ.get("SEARCH_API_KEY")

    async with AsyncExitStack() as stack:
        if api_key:
            credential = AzureKeyCredential(api_key)
        else:
            credential = await stack.enter_async_context(AzureCliCredential())

        client = await stack.enter_async_context(
            KnowledgeBaseRetrievalClient(
                endpoint=endpoint,
                credential=credential,
                knowledge_base_name=knowledge_base_name,
            )
        )
        response = await client.retrieve(
            KnowledgeBaseRetrievalRequest(
                intents=[KnowledgeRetrievalSemanticIntent(search=query)],
                knowledge_source_params=[
                    AzureBlobKnowledgeSourceParams(
                        knowledge_source_name=knowledge_source_name,
                        include_references=True,
                    )
                ],
            )
        )

    answer_parts = [
        content.text
        for message in (response.response or [])
        for content in (message.content or [])
        if getattr(content, "text", None)
    ]

    citations = sorted(
        {
            getattr(ref, "blob_url", None) or ref.id
            for ref in (response.references or [])
            if getattr(ref, "type", None) == "azureBlob"
        }
    )

    answer = "\n".join(answer_parts) or "No grounded answer was found in the knowledge base."
    if citations:
        answer += "\n\nSources:\n" + "\n".join(f"- {c}" for c in citations)
    return answer
