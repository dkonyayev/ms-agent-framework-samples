# Build a calculator agent using the LangGraph Graph aPI
# Before running
# 1. Install the required packages:
#    pip install IPython langchain langgraph langchain-anthropic
# 2. In termainal run <$env:ANTHROPIC_API_KEY = "your_anthropic_api_key">


# Sample Response
# The sum of 3 and 4 is **7**.
# The result of multiplying 7 by 2 is **14**.

from langchain.tools import tool
from langchain.chat_models import init_chat_model


model = init_chat_model(
    "claude-sonnet-4-6",
    temperature=0
)


# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a / b


# Augment the LLM with tools
tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)


# DEFINE STATE
# The graph’s state is used to store the messages and the number of LLM calls.
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int



# DEFINE MODEL NODE
# The model node is used to call the LLM and decide whether to call a tool or not.
from langchain.messages import SystemMessage
def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }


# DEFINE TOOL NODE
# The tool node is used to call the tools and return the results.
from langchain.messages import ToolMessage
def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


# DEFINE END LOGIC
# The conditional edge function is used to route to the tool node or end based upon whether the LLM made a tool call.
from typing import Literal
from langgraph.graph import StateGraph, START, END


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END




# BUILD AND COMPILE AGENT
# The agent is built using the StateGraph class and compiled using the compile method.

from langgraph.checkpoint.memory import MemorySaver

# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent
memory = MemorySaver()
agent = agent_builder.compile(checkpointer=memory)


# Show the agent
from IPython.display import Image, display
display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

# Invoke
from langchain.messages import HumanMessage

# Invoke using the same thread ID
config = {"configurable": {"thread_id": "calculator-session"}}

first_response = agent.invoke(
    {"messages": [HumanMessage(content="Add 3 and 4.")]},
    config,
)

second_response = agent.invoke(
    {"messages": [HumanMessage(content="Multiply that result by 2.")]},
    config,
)

for message in second_response["messages"]:
    message.pretty_print()