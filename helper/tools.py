"""Research Tools.

This module provides search and content processing tools for the research agent,
including search/summarization tool and thinking tool.
"""

from pydantic import BaseModel
from langchain_core.tools import tool

from helper.utils import tavily_search_multiple, deduplicate_search_results, process_search_results, format_search_output


@tool
def tavily_search(
    query: str,
) -> str:
    """Fetch results from Tavily search API with content summarization.

    Args:
        query: A single search query to execute

    Returns:
        Formatted string of search results with summaries
    """
    # Execute search for single query
    search_results = tavily_search_multiple(
        [query],  # Convert single query to list for the internal function
        max_results=3,
        topic="general",
        include_raw_content=True,
    )

    # Deduplicate results by URL to avoid processing duplicate content
    unique_results = deduplicate_search_results(search_results)

    # Process results with summarization
    summarized_results = process_search_results(unique_results)

    # Format output for consumption
    return format_search_output(summarized_results)

@tool
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.
    
    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.
    
    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?
    
    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?
    
    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps
        
    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"

@tool(parse_docstring=True)
def ConductResearch(research_topic: str) -> str:
    """Tool for delegating a research task to a specialized sub-agent.
    
    Use this tool when you need to conduct in-depth research on a specific topic.
    This tool delegates the research to a specialized sub-agent that will:
    - Search for relevant information using multiple sources
    - Analyze and synthesize findings
    - Provide comprehensive research results
    
    When to use:
    - When you need detailed information on a specific topic
    - When the user asks for research, analysis, or investigation
    - When you need to gather facts, data, or examples
    - When comparing different approaches, technologies, or methods
    
    How to use:
    - Provide a clear, specific research topic
    - Include sufficient detail (at least a paragraph) for comprehensive research
    - Focus on one specific topic per tool call
    - Use multiple tool calls for parallel research on different aspects
    
    Args:
        research_topic: The topic to research. Should be a single topic, and should be described in high detail (at least a paragraph).
    """
    return f"Research task delegated for topic: {research_topic}"

@tool
class ResearchComplete(BaseModel):
    """Tool for indicating that the research process is complete."""
    pass