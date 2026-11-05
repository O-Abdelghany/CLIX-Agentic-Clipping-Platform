from app.graph.llm import llm
from app.graph.state import State

AUDIO_EXTENSIONS = (".mp3", ".mp4", ".wav", ".m4a", ".ogg", ".flac", ".webm")

def orchestrator(state: State) -> State:
    last_message = state["messages"][-1]
    content = last_message.content if hasattr(last_message, "content") else last_message["content"]

    if any(content.strip().endswith(ext) for ext in AUDIO_EXTENSIONS):
        return {"next": "transcription"}

    system_prompt = (
        "You are an orchestrator agent. Your job is to understand the user's request "
        "and decide how to route it to the appropriate tools or agents."
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response], "next": "end"}
