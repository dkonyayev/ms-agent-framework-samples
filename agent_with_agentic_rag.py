# Sample: a Foundry agent grounded in a fictional company's knowledge base via
# Azure AI Search agentic retrieval (Knowledge Base), used as a tool.
#
# Before running:
# 1. Install the required packages:
#    pip install azure-identity azure-search-documents agent-framework
# 2. Complete "az login" (see .env for tenant details).
# 3. SEARCH_ENDPOINT / KNOWLEDGE_BASE_NAME / KNOWLEDGE_SOURCE_NAME are already
#    set in .env for this project — see Documentation/foundry-rag-agent/plan.md
#    §4A for how the Azure resources were provisioned.

import asyncio

from dotenv import load_dotenv
from agent_framework import Agent

from foundry_client import create_foundry_client
from tools.knowledge_base_search import search_meridian_knowledge_base

load_dotenv()


async def main() -> None:
    agent = Agent(
        client=create_foundry_client(),
        name="MeridianSupportAgent",
        instructions=(
            "You are a support assistant for Meridian Cloudworks. Use the "
            "search_meridian_knowledge_base tool to answer questions about "
            "Meridian Flow's product, pricing, HR policies, and support FAQs. "
            "Only answer from the tool's results, and mention the source "
            "document. If the tool doesn't have the answer, say you don't know."
        ),
        tools=[search_meridian_knowledge_base],
    )

    result = await agent.run("How many PTO days do new hires get?")
    print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
