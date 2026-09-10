# Expose python function to model as callable tool
# Before running
# 1. Install the required packages:
#    pip install azure-identity agent-framework
# 2. Set up your Foundry project and get the project endpoint URL.
# 3. Update the project_endpoint to variable FOUNDRY_PROJECT_ENDPOINT in .env 
# 4. Complete "az login" in terminal (author - see .env for additional details)

# Sample Response
# Agent: The weather in Tampa, FL today is sunny with a high temperature of 14°C.

import asyncio
from dotenv import load_dotenv
from agent_framework import Agent

from foundry_client import create_foundry_client
from tools.get_weather import get_weather

load_dotenv()

async def main() -> None:

    agent = Agent(
        client=create_foundry_client(),
        name="WeatherAgent",
        instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
        tools=[get_weather],
    )

    result = await agent.run("What is the weather today in Tampa, FL?")
    print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())

