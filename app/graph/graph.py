from langgraph.graph import StateGraph, START, END
from app.graph.state import State
from app.agents.orchestrator import orchestrator
from app.agents.transcription_agent import transcription_agent
from app.agents.chatting_agent import chatting_agent
from app.graph.routing import route

builder = StateGraph(State)

builder.add_node("orchestrator", orchestrator)
builder.add_node("transcription", transcription_agent)
builder.add_node("chatting_agent", chatting_agent)

builder.add_edge(START, "orchestrator")
builder.add_conditional_edges("orchestrator", route, {"transcription": "transcription", "chat": "chatting_agent"})
builder.add_edge("transcription", END)
builder.add_edge("chatting_agent", END)

graph = builder.compile()