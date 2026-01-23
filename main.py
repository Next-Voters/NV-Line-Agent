import asyncio

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from phases.research_scope import clarify_with_user, write_research_brief
from phases.lead_researcher import supervisor_agent
from helper.state_config import AgentState, AgentInputState

agent = None

def build_agent_graph():
    global agent
    agent_builder = StateGraph(AgentState, input_state=AgentInputState)
    agent_builder.add_node("clarify_with_user", clarify_with_user)
    agent_builder.add_node("write_research_brief", write_research_brief)


    agent_builder.add_edge(START, "clarify_with_user")
    agent_builder.add_edge("write_research_brief", END)

    # Checkpointer saves messages even after agent runs once
    checkpointer = InMemorySaver()
    agent = agent_builder.compile(checkpointer=checkpointer)

async def run_agent():
    message = input("User: ")
    # Use unique thread_id to avoid state contamination
    thread = {"configurable": {"thread_id": f"thread_{hash(message)}", "recursion_limit": 50}}
    result = await agent.ainvoke({"messages": [HumanMessage(content=message)]}, config=thread)
    return result

async def main_loop():
    build_agent_graph()
    while True:
        result = await run_agent()
        
        if bool(result.get('research_brief', {})):
            print(result.get('research_brief'))
            break
        else:
            print(result.get('messages', [])[-1].content)

    print(result.get('messages', [])[-1].content)


if __name__ == "__main__":
    asyncio.run(main_loop())
