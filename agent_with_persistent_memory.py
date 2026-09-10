# Use session to maintain conversation context
# Before running
# 1. Install the required packages:
#    pip install azure-identity agent-framework
# 2. Set up your Foundry project and get the project endpoint URL.
# 3. Update the project_endpoint to variable FOUNDRY_PROJECT_ENDPOINT in .env 
# 4. Complete "az login" in terminal (author - see .env for additional details)

# Sample Response
# Agent: Hi Alice! That’s awesome—hiking is a fantastic way to explore nature and stay active. Do you have a favorite trail?
# Agent: You mentioned your name is Alice and that you love hiking!

import asyncio
from dotenv import load_dotenv
from agent_framework import Agent

from foundry_client import create_foundry_client
from providers.user_memory_provider import UserMemoryProvider

load_dotenv()

async def main() -> None:

    client = create_foundry_client()

    agent = Agent(
        client=client,
        name="MemoryAgent",
        instructions="You are a friendly assistant.",
        context_providers=[UserMemoryProvider()],
    )

    # Create a session to maintain conversation history
    session = agent.create_session()

    # The provider doesn't know the user yet — it will ask for a name
    result = await agent.run("Hello! What's the square root of 9?", session=session)
    print(f"Agent: {result}\n")

    # Now provide the name — the provider stores it in session state
    result = await agent.run("My name is Alice", session=session)
    print(f"Agent: {result}\n")

    # Subsequent calls are personalized — name persists via session state
    result = await agent.run("What is 2 + 2?", session=session)
    print(f"Agent: {result}\n")

    # Inspect session state to see what the provider stored
    provider_state = session.state.get("user_memory", {})
    print(f"[Session State] Stored user name: {provider_state.get('user_name')}")

if __name__ == "__main__":
    asyncio.run(main())

