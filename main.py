"""
Main Research Agent Orchestrator.

This module serves as the primary entry point and workflow orchestrator for the NV-Line-Agent research system.
It coordinates two distinct phases of operation:

1. Research Scope Clarification Phase:
   - Interacts with user to gather and refine research requirements
   - Generates comprehensive research briefs from user input
   - Limits clarification exchanges to maintain efficiency

2. Research Execution Phase:
   - Executes the actual research using supervisor and researcher agents
   - Coordinates between multiple specialized sub-agents
   - Generates final research reports

Architecture:
- Uses LangGraph for workflow management and state tracking
- Implements async/await patterns for non-blocking execution
- Maintains separate agent instances for different workflow phases
- Uses InMemorySaver for state persistence within sessions

Usage:
    python main.py

The system will prompt for user input and guide them through the complete research process,
from initial scoping to final report generation.
"""

import asyncio

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from phases.research_scope import clarify_with_user, write_research_brief
from phases.research_execution.lead_researcher import supervisor_agent
from phases.research_execution.writer import final_report_generation, save_final_report

from helper.state_config import ResearchScopeState, ResearchExecutionState, AgentInputState, AgentState

# Global agent instances for different workflow phases
research_brief_agent = None
research_agent = None

def build_research_scope_graph():
    """
    Build and compile the research scope clarification workflow graph.
    
    This function creates a LangGraph workflow that handles:
    - User input clarification through iterative questioning
    - Research brief generation from conversation history
    - State management for the clarification phase
    
    The graph consists of two nodes:
    1. 'clarify_with_user': Determines if clarification is needed and asks questions
    2. 'write_research_brief': Generates comprehensive research brief
    
    Workflow: START → clarify_with_user → write_research_brief → END
    
    Args:
        None
        
    Returns:
        None (compiles graph into global research_brief_agent variable)
        
    Side Effects:
        Sets global research_brief_agent with compiled graph instance
    """
    global research_brief_agent
    agent_builder = StateGraph(ResearchScopeState, input_state=AgentInputState)
    agent_builder.add_node("clarify_with_user", clarify_with_user)
    agent_builder.add_node("write_research_brief", write_research_brief)

    agent_builder.add_edge(START, "clarify_with_user")
    agent_builder.add_edge("write_research_brief", END)

    # Checkpointer saves messages even after agent runs once
    checkpointer = InMemorySaver()
    research_brief_agent = agent_builder.compile(checkpointer=checkpointer)


def build_research_execution_graph():
    """
    Build and compile the main research execution workflow graph.
    
    This function creates a LangGraph workflow that handles:
    - Supervisor agent coordination for research tasks
    - Final report generation from research findings
    - Integration with researcher sub-agents for data collection
    
    The graph consists of two nodes:
    1. 'supervisor_subgraph': Coordinates research execution and delegates tasks
    2. 'final_report_generation': Synthesizes findings into final report
    
    Workflow: START → supervisor_subgraph → final_report_generation → END
    
    Args:
        None
        
    Returns:
        None (compiles graph into global research_agent variable)
        
    Side Effects:
        Sets global research_agent with compiled graph instance
    """
    global research_agent
    agent_builder = StateGraph(AgentState, input_state=AgentInputState)
    agent_builder.add_node("supervisor_subgraph", supervisor_agent)
    agent_builder.add_node("final_report_generation", final_report_generation)
    agent_builder.add_node("save_final_report", save_final_report)

    agent_builder.add_edge(START, "supervisor_subgraph")
    agent_builder.add_edge("supervisor_subgraph", "final_report_generation")    
    agent_builder.add_edge("final_report_generation", "save_final_report")
    agent_builder.add_edge("save_final_report", END)

    # Checkpointer saves messages even after agent runs once
    checkpointer = InMemorySaver()
    research_agent = agent_builder.compile(checkpointer=checkpointer)

async def execute_research_scope_phase():
    """
    Execute the research scope clarification phase with user interaction.
    
    This function handles the interactive clarification loop where:
    - Prompts user for initial research request
    - Executes research scope clarification graph
    - Processes user responses until research brief is generated
    - Manages thread isolation to prevent state contamination
    
    Args:
        None (gets user input via stdin)
        
    Returns:
        dict: Result from research_brief_agent containing either:
            - 'research_brief': Generated research brief (if clarification complete)
            - 'messages': Clarification questions (if more info needed)
            
    Thread Management:
        Uses hash-based thread_id for isolation between sessions
        
    State Flow:
        User input → research_brief_agent → result analysis → continue/exit
    """
    message = input("User: ")
    # Use unique thread_id to avoid state contamination
    thread = {"configurable": {"thread_id": f"thread_{hash(message)}", "recursion_limit": 50}}
    result = await research_brief_agent.ainvoke({"messages": [HumanMessage(content=message)]}, config=thread)
    return result

async def execute_research_phase(research_brief: str):
    """
    Execute the main research and report generation phase.
    
    This function handles the core research execution where:
    - Coordinates supervisor and researcher sub-agents
    - Executes actual data collection and analysis
    - Generates final research report
    - Uses research brief from previous phase as input
    
    Args:
        research_brief: Research brief generated from scope clarification phase
        
    Returns:
        dict: Result from research_agent containing:
            - 'final_report': Generated research report
            - 'messages': Status messages
            
    Thread Management:
        Uses unique thread_id based on research brief agent state
        Prevents interference with scope clarification phase
        
    State Flow:
        Research brief → supervisor_subgraph → final_report_generation → result
    """
    # Use unique thread_id to avoid state contamination
    thread = {"configurable": {"thread_id": f"research_execution_{hash(research_brief)}", "recursion_limit": 50}}
    result = await research_agent.ainvoke({
        "messages": [HumanMessage(content=research_brief)], 
        "research_brief": research_brief
    }, config=thread)
    return result

async def main_research_workflow():
    """
    Main orchestrator for the complete research workflow.
    
    This function coordinates the entire research process through two distinct phases:
    
    Phase 1 - Research Scope Clarification:
        - Builds and executes scope clarification graph
        - Iterates with user until sufficient context gathered
        - Generates comprehensive research brief
        - Limits clarification to maintain efficiency
        
    Phase 2 - Research Execution:
        - Builds and executes research workflow graph
        - Coordinates supervisor and researcher agents
        - Generates final comprehensive report
        - Presents results to user
        
    Error Handling:
        - Maintains isolation between phases
        - Uses unique thread identifiers
        - Graceful handling of user interruptions
        
    Args:
        None
        
    Returns:
        None (prints results to stdout)
        
    Side Effects:
        - Prints research brief when generated
        - Prints final research report
        - Manages user interaction flow
    """  
    research_brief = None  
    # Phase 1: Research Scope Clarification
    build_research_scope_graph()
    while True:
        result = await execute_research_scope_phase()
        
        if bool(result.get('research_brief', {})):
            research_brief = result.get('research_brief')
            print('💼 Research Brief: ', result.get('research_brief'))
            break
        else:
            print(result.get('messages', [])[-1].content)

    # Phase 2: Research Execution and Report Generation
    build_research_execution_graph()
    print("🧠 Researching and generating report...")
    result = await execute_research_phase(research_brief)
    print(result.get('messages', [])[-1].content)


if __name__ == "__main__":
    asyncio.run(main_research_workflow())
