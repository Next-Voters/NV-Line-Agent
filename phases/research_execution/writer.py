"""Writer Component

This module implements the final report generation phase of the research workflow, where we:
1. Synthesize all research findings into a comprehensive final report
2. Generate the final report using the research brief and findings
"""

from langchain_core.messages import HumanMessage

from helper.utils import get_today_str
from helper.prompts import final_report_generation_prompt
from helper.state_config import AgentState

from langchain.chat_models import init_chat_model
writer_model = init_chat_model(model="openai:gpt-4.1", max_tokens=32000) 

async def final_report_generation(state: AgentState):
    """
    Final report generation node.
    
    Synthesizes all research findings into a comprehensive final report
    """
    
    notes = state.get("notes", [])
    
    findings = "\n".join(notes)

    final_report_prompt = final_report_generation_prompt.format(
        research_brief=state.get("research_brief", ""),
        findings=findings,
        date=get_today_str()
    )
    
    final_report = await writer_model.ainvoke([HumanMessage(content=final_report_prompt)])
    
    return {
        "final_report": final_report.content, 
        "messages": ["Here is the final report: " + final_report.content],
    }

async def save_final_report(state: AgentState):
    """
    Save the final report to a file
    """
    with open("final_report.md", "w") as f:
        f.write(state["final_report"])
    return {
        "messages": ["Final report saved to final_report.md"]
    }