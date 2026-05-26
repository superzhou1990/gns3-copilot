# SPDX-License-Identifier: GPL-3.0-or-later
#
# GNS3-Copilot - Unified Agent for Multiple Network Simulators
#

"""
Unified Network Automation Agent

Supports multiple network simulation platforms through platform abstraction.
Maintains identical interface regardless of underlying simulator.
"""

import operator
import sqlite3
from typing import Annotated, Literal

import streamlit as st
from langchain.messages import AnyMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.managed.is_last_step import RemainingSteps
from typing_extensions import TypedDict

from gns3_copilot.agent.model_factory import (
    create_base_model_with_tools,
    create_title_model,
)
from gns3_copilot.log_config import setup_logger
from gns3_copilot.platform_abstraction import (
    PlatformFactory,
    get_current_platform,
)
from gns3_copilot.prompts import TITLE_PROMPT, load_system_prompt
from gns3_copilot.utils import get_config

logger = setup_logger("unified_agent")

# Get current platform and load appropriate tools
CURRENT_PLATFORM = get_current_platform()
tools = PlatformFactory.get_all_tools(CURRENT_PLATFORM)
tools_by_name = {tool.name: tool for tool in tools}

logger.info(
    "Unified Agent initialized for platform: %s with %d tools",
    CURRENT_PLATFORM.value,
    len(tools),
)


# Define state (same as GNS3 version)
class MessagesState(TypedDict):
    """Conversation state management."""

    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
    remaining_steps: RemainingSteps
    conversation_title: str | None
    selected_project: tuple[str, str, int, int, str] | None
    topology_info: dict | None
    platform: str  # Track current platform


# Define llm call node
def llm_call(state: dict):
    """LLM decides whether to call a tool or not."""
    current_prompt = load_system_prompt()

    selected_p = state.get("selected_project")
    context_messages = []
    topology_info = None

    if selected_p:
        # Platform-agnostic project info
        project_info = (
            "User has selected project: "
            f"Project_Name={selected_p[0]}, "
            f"Project_ID={selected_p[1]}, "
            f"Device_Number={selected_p[2]}, "
            f"Link_Number={selected_p[3]}, "
            f"Status={selected_p[4]}"
        )
        logger.debug("Project info for LLM context: %s", project_info)

        # Get topology tool for current platform
        topology_tool = PlatformFactory.get_topology_tool(CURRENT_PLATFORM)

        try:
            topology = topology_tool._run(project_id=selected_p[1])

            if topology and "error" not in topology:
                topology_info = topology
                logger.info("Successfully retrieved topology: %s", selected_p[0])

                topology_context = str(topology)
                context_messages.append(
                    SystemMessage(
                        content=f"Current Context: {project_info}\n\nTopology:\n{topology_context}"
                    )
                )
            else:
                logger.warning("Failed to retrieve topology: %s", topology.get("error"))
                context_messages.append(
                    SystemMessage(content=f"Current Context: {project_info}")
                )
        except Exception as e:
            logger.warning("Error retrieving topology: %s", e)
            context_messages.append(
                SystemMessage(content=f"Current Context: {project_info}")
            )

    full_messages = [SystemMessage(content=current_prompt)] + context_messages + state["messages"]

    model_with_tools = create_base_model_with_tools(tools)

    return {
        "messages": [model_with_tools.invoke(full_messages)],
        "llm_calls": state.get("llm_calls", 0) + 1,
        "topology_info": topology_info,
    }


def generate_title(state: MessagesState) -> dict:
    """Generate conversation title."""
    if state.get("conversation_title") in [None, "New Session"]:
        messages = state["messages"]

        title_prompt_messages = [
            SystemMessage(content=TITLE_PROMPT),
            messages[0],
            messages[-1],
        ]

        try:
            title_model = create_title_model()
            response = title_model.invoke(
                title_prompt_messages, config={"configurable": {"foo_temperature": 1.0}}
            )

            new_title = response.content.strip()

            if len(new_title) > 40:
                new_title = new_title[:38] + "..."

            new_title = new_title.replace("\n", " ").replace('"', "").replace("'", "")

            if not new_title:
                new_title = "Network Session"

            logger.info("Generated title: %s", new_title)
            return {"conversation_title": new_title}

        except Exception as e:
            logger.error("Title generation failed: %s", e)
            return {"conversation_title": "Untitled Session"}

    return {}


def tool_node(state: dict):
    """Execute tools."""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


def should_continue(state: MessagesState) -> Literal["tool_node", "title_generator_node", END]:
    """Route after LLM response."""
    last_message = state["messages"][-1]
    current_title = state.get("conversation_title")

    if last_message.tool_calls:
        logger.debug("LLM requested tool calls → routing to tool_node")
        return "tool_node"

    if current_title in [None, "Network Session"]:
        logger.info("First turn completed → routing to title_generator_node")
        return "title_generator_node"

    logger.debug("Conversation complete → routing to END")
    return END


def recursion_limit_continue(state: MessagesState) -> Literal["llm_call", END]:
    """Check recursion limit after tool execution."""
    last_message = state["messages"][-1]
    if isinstance(last_message, ToolMessage):
        if state["remaining_steps"] < 4:
            return END
        return "llm_call"

    return END


# Build and compile the agent
agent_builder = StateGraph(MessagesState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_node("title_generator_node", generate_title)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "tool_node": "tool_node",
        "title_generator_node": "title_generator_node",
        END: END,
    },
)
agent_builder.add_conditional_edges(
    "tool_node",
    recursion_limit_continue,
    {
        "llm_call": "llm_call",
        END: END,
    },
)
agent_builder.add_edge("title_generator_node", END)

# Persistence
LANGGRAPH_DB_PATH = "gns3_langgraph.db"


@st.cache_resource(show_spinner="Initializing conversation persistence...")
def get_checkpointer() -> SqliteSaver:
    """Create and cache checkpointer."""
    conn = sqlite3.connect(LANGGRAPH_DB_PATH, check_same_thread=False)
    return SqliteSaver(conn)


@st.cache_resource(show_spinner="Compiling unified agent...")
def get_agent():
    """Compile and cache agent."""
    return agent_builder.compile(checkpointer=get_checkpointer())


langgraph_checkpointer = get_checkpointer()
agent = get_agent()

logger.info("Unified Agent ready for platform: %s", CURRENT_PLATFORM.value)
