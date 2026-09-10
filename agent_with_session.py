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
from tools.get_weather import get_weather

load_dotenv()

async def main() -> None:

    client = create_foundry_client()

    agent = Agent(
        client=client,
        name="ConversationAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )

    # Create a session to maintain conversation history
    session = agent.create_session()

    # First turn
    result = await agent.run("My name is Alice and I love hiking.", session=session)
    print(f"Agent: {result}\n")

    # Second turn — the agent should remember the user's name and hobby
    result = await agent.run("What do you remember about me?", session=session)
    print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())

