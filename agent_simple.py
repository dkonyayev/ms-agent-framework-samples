# Sample python to demonstrate how to create a simple agent using FoundryChatClient and run it in both non-streaming and streaming modes.
# Before running
# 1. Install the required packages:
#    pip install azure-identity agent-framework
# 2. Set up your Foundry project and get the project endpoint URL.
# 3. Update the project_endpoint and tenant_id in the code below with your own values.
# 4. Complete login for koveent@gmail.com
#    az login --tenant 13f0df60-549e-4639-82ef-3a1ad3f3b4a1

# Sample Response
# Agent: The capital of France is Paris.
import asyncio

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential



"""
Hello Agent — Simplest possible agent

This sample creates a minimal agent using FoundryChatClient via an
Microsoft Foundry project endpoint, and runs it in both non-streaming and streaming modes.

There are XML tags in all of the get started samples, those are used to display the same code in the docs repo.
"""
async def main() -> None:

    # <create_agent>
    client = FoundryChatClient(
        project_endpoint="https://ai-kove-foundry-sandbox.services.ai.azure.com/api/projects/proj-default",
        model="gpt-4o",
        credential=AzureCliCredential()
    )

    agent = Agent(
        client=client,
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    # </create_agent>

    # <run_agent>
    # Non-streaming: get the complete response at once
    result = await agent.run("What is the capital of France?")
    print(f"Agent: {result}")
    # </run_agent>

    # <run_agent_streaming>
    # Streaming: receive tokens as they are generated
    print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run("Tell me a one-sentence fun fact.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()
    # </run_agent_streaming>

    

if __name__ == "__main__":
    asyncio.run(main())

