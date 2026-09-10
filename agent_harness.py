# Use session to maintain conversation context
# Before running
# 1. Install the required packages:
#    pip install azure-identity agent-framework
# 2. Set up your Foundry project and get the project endpoint URL.
# 3. Update the project_endpoint to variable FOUNDRY_PROJECT_ENDPOINT in .env 
# 4. Complete "az login" in terminal (author - see .env for additional details)

# Console (in this sample) is just a tiny helper module that makes the harness examples 
# easier to run. It wraps simple things like printing messages nicely, reading user input, 
# formatting agent output, and showing tool calls in a clean, readable way. It isn’t part of 
# Python or the agent framework — it’s just a lightweight utility the sample authors 
# wrote so the demo agent feels like a small “CLI app” instead of raw print statements.
# Python does have logging framework, but console in this case is a small wrapper for printing
# colored text

# Harness = a control layer that wraps an agent with planning, memory,
# tool routing, retries, and safety so it can run multi‑step tasks
# reliably. A normal agent is just “LLM + prompt”; a harnessed agent
# is structured, stateful, and predictable. Use it for autonomous
# workflows, not simple one‑shot prompts.

# Sample Response
# Agent: Hi Alice! That’s awesome—hiking is a fantastic way to explore nature and stay active. Do you have a favorite trail?
# Agent: You mentioned your name is Alice and that you love hiking!

import asyncio
from dotenv import load_dotenv

from agent_framework import (
    create_harness_agent,
    todos_remaining,
    todos_remaining_message,
)

from console import build_observers_with_planning, run_agent_async
from foundry_client import create_foundry_client


load_dotenv()

RESEARCH_INSTRUCTIONS = """\
## Research Assistant Instructions

You are a research assistant. When given a research topic, research it
thoroughly using web search and web browsing. Use your knowledge to form good
search queries and hypotheses, but always verify claims with the tools
available to you rather than relying on memory alone.

### Research quality

Consult multiple sources when possible and cross-reference key claims.
When sources disagree, note the discrepancy and explain which source you
consider more reliable and why.
If a web page fails to load or a search returns irrelevant results, try
alternative search queries or sources before moving on.
Track your sources — you will need them when presenting results.

### Presenting results

When presenting your final findings:
- Use Markdown formatting for clarity.
- Use clear sections with headings for each major topic or sub-question.
- Cite your sources inline (e.g., "According to [source name](URL), ...").
- End with a brief summary of key takeaways.
- In addition to returning the results to the user, save the final research
  report to file memory so it survives compaction and can be referenced later.
"""

async def main() -> None:

    client = create_foundry_client()

    # Create a harness agent with research-specific instructions.
    # All other features (todo, mode, compaction, skills, telemetry, web search) are
    # automatically configured with sensible defaults.
    agent = create_harness_agent(
        client=client,
        max_context_window_tokens=128_000,
        max_output_tokens=16_384,
        name="ResearchAgent",
        description="A research assistant that plans and executes research tasks.",
        agent_instructions=RESEARCH_INSTRUCTIONS,
        # Enable harness looping: while the agent is in "execute" mode and still has open todos,
        # keep re-invoking it automatically so it works through the whole plan without manual
        # prompting. loop_next_message reminds the agent which todos are still open each pass, and
        # loop_max_iterations caps the autonomous passes per turn as a safety net.
        loop_should_continue=todos_remaining(looping_modes=["execute"]),
        loop_next_message=todos_remaining_message,
        loop_max_iterations=10,
    )

    # Run the harness console with the research agent.
    await run_agent_async(
        agent,
        session=agent.create_session(),
        observers=build_observers_with_planning(agent),
        initial_mode="plan",
        title="🔬 Research Assistant",
        placeholder="Enter a research topic...",
        max_context_window_tokens=128_000,
        max_output_tokens=16_384,
    )

if __name__ == "__main__":
    asyncio.run(main())

