import os
from typing import TypedDict, Annotated, List, Literal
from typing import Dict, List, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
# from langgraph.prebuilt import create_react_agent

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

# lets import the agents here to avoid circular imports
from agents.supervisor_agent import supervisor_agent
from agents.research_agent import researcher_agent
from agents.analysis_agent import analyst_agent
from agents.writing_agent import writer_agent

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")


llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")


# ===================================
# State import
# ===================================

from state.supervisorstate import SupervisorState


# router function to call the right agent based on supervisor's decision

def router(state: SupervisorState) -> Literal["supervisor", "researcher", "analyst", "writer", "__end__"]:
    """Routes to next agent based on state"""
    
    next_agent = state.get("next_agent", "supervisor")
    
    if next_agent == "end" or state.get("task_complete", False):
        return END
        
    if next_agent in ["supervisor", "researcher", "analyst", "writer"]:
        return next_agent
        
    return "supervisor"


# Create workflow/graph

def create_workflow():

    workflow = StateGraph(SupervisorState)
    memory = MemorySaver()
    # Add nodes
    workflow.add_node("supervisor", lambda state: supervisor_agent(state,llm))
    workflow.add_node("researcher", lambda state: researcher_agent(state,llm))
    workflow.add_node("analyst", lambda state: analyst_agent(state,llm))
    workflow.add_node("writer", lambda state: writer_agent(state,llm))

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Add routing
    for node in ["supervisor", "researcher", "analyst", "writer"]:
        workflow.add_conditional_edges(
            node,
            router,
            {
                "supervisor": "supervisor",
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                END: END  # map the END sentinel to the workflow END target
            }
        )

    return workflow.compile(checkpointer=memory)

# Build once
graph = create_workflow()



from langchain_core.messages import HumanMessage, AIMessage

def get_conversation(site_id: str):
    """
    Fetch conversation history from LangGraph memory
    for UI rendering only.
    """

    config = {
        "configurable": {
            "thread_id": site_id
        }
    }

    checkpoint_tuple = graph.checkpointer.get_tuple(config)

    if not checkpoint_tuple:
        return []

    # 👇 checkpoint is ALWAYS at index 1
    checkpoint = checkpoint_tuple[1]

    messages = checkpoint.get("channel_values", {}).get("messages", [])

    chat = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            chat.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            chat.append({"role": "assistant", "content": msg.content})

    return chat



# lets now create a function to run the graph with a given task
def run_task(task: str, site_id: str) -> str:
    """
    Runs the multi-agent system using LangGraph memory.
    Memory is tracked per site_id (thread_id).
    """

    result = graph.invoke(
        {
            "messages": [HumanMessage(content=task)],
            "current_task": task
        },
        config={
            "configurable": {
                "thread_id": site_id   # ✅ correct place
            }
        }
    )
    # print("Final result from graph:", result.get("final_report"))
    return result.get("final_report", "No report generated.")





