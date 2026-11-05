from app.graph.llm import llm
from app.graph.state import State
from app.system_prompt.chat_prompt import CHAT_SYSTEM_PROMPT

def chatting_agent(state: State) -> dict:
    messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response], "route_to": "end"}