"""Research ReAct Agent.
The agent will execute different tools (which will create a chain of reasoning and results) and conduct reasoning for each tool execution. 
This will happen iteratively until the agent is satisfied with the result.
"""

from langchain.chat_models import init_chat_model
from helper.prompts import research_agent_prompt
from helper.state_config import model
from dotenv import load_dotenv

load_dotenv()

tools = [
    'tavily_search',
    'think_tool'
]

model = init_chat_model(model="openai:gpt-5-mini", temperature=0.0)
model_with_tools = model.bind_tools(tools)

def llm_call(state: ResearcherState):
    """Analyze current state and decide on next actions.
    
    The model analyzes the current conversation state and decides whether to:
    1. Call search tools to gather more information
    2. Provide a final answer based on gathered information
    
    Returns updated state with the model's response.
    """
    return {
        "researcher_messages": [
            model_with_tools.invoke(
                [SystemMessage(content=research_agent_prompt)] + state["researcher_messages"]
            )
        ]
    }

