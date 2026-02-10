"""Writer Component

This module implements the final report generation phase of the research workflow, where we:
1. Synthesize all research findings into a comprehensive final report
2. Generate the final report using the research brief and findings
3. Save the final report to cloud storage (Supabase)
"""

import os
from supabase import create_client, Client
from datetime import datetime
from langchain_core.messages import HumanMessage

from helper.utils import get_today_str
from helper.prompts import final_report_generation_prompt
from helper.state_config import AgentState

from langchain.chat_models import init_chat_model
writer_model = init_chat_model(model="openai:gpt-4o", max_tokens=16384) 

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

def save_final_report(state: AgentState):
    """
    Save the final report to cloud storage (Supabase only)
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        return {
            "messages": ["Error: SUPABASE_URL and SUPABASE_KEY must be set in environment variables"]
        }
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        
        filename = f"final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        storage_path = f"nv-line-agent/{filename}"
        
        supabase.storage.from_("reports").upload(
            path=storage_path,
            file=state["final_report"].encode('utf-8'),
            file_options={"content-type": "text/markdown"}
        )
        
        try:
            public_url = supabase.storage.from_("reports").get_public_url(storage_path)
            message = f"Final report uploaded to Supabase: {public_url}"
        except:
            message = f"Final report uploaded to Supabase: {storage_path}"
        
        return {
            "messages": [message]
        }
        
    except Exception as e:
        return {
            "messages": [f"Failed to upload to Supabase: {e}"]
        }