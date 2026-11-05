from langgraph.graph import StateGraph, START, END
from app.graph.state import State
from app.agents.orchestrator import orchestrator
from app.agents.transcription_agent import transcription_agent


builder = StateGraph(State)

builder.add_node("orchestrator", orchestrator)
builder.add_node("transcription", transcription_agent)


builder.add_edge(START, "orchestrator")
builder.add_edge("orchestrator", "transcription")

graph = builder.compile()