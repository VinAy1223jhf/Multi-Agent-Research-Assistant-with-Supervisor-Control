# ===================================
# Agent 3: Writer (FIXED)
# ===================================
import datetime
from langchain_core.messages import HumanMessage, AIMessage
from state.supervisorstate import SupervisorState


def writer_agent(state, llm):
    research_data = state.get("research_data", "")
    analysis = state.get("analysis", "")
    task = state.get("current_task", "")

    writing_prompt = f"""As a professional writer, create an executive report based on:

Task: {task}

Research Findings:
{research_data[:1000]}

Analysis:
{analysis[:1000]}
"""

    report_response = llm.invoke([HumanMessage(content=writing_prompt)])
    report = report_response.content

    final_report = f"""
📄 FINAL REPORT
{'='*50}
Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{'='*50}

{report}
"""

    return {
        "final_report": final_report,
        "messages": [
            AIMessage(content=final_report)
        ],
        "task_complete": True,
        "next_agent": "end"
    }

