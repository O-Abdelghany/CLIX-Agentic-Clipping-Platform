import whisper
from app.graph.state import State

model = whisper.load_model("tiny") #future use we may use turbo as it has better accuracy


def transcription_agent(state: State) -> dict:
    last_message = state["messages"][-1]
    audio_path = last_message.content if hasattr(last_message, "content") else last_message["content"]

    result = model.transcribe(audio_path)

    detected_language = result.get("language", "unknown")
    text = result["text"]

    return {
    "messages": [{"role": "assistant", "content": f"Detected language: {detected_language}\n\nTranscription:\n{text}"}],
    "route_to": "end"
}

