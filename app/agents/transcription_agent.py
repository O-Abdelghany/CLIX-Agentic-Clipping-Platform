import os
from groq import Groq
from app.graph.state import State
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcription_agent(state: State) -> State:
    # Extract the audio file path from the last user message
    last_message = state["messages"][-1]
    audio_path = last_message.content if hasattr(last_message, "content") else last_message["content"]

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            response_format="text"
        )

    return {
        "messages": [{"role": "assistant", "content": f"Transcription:\n{transcription}"}]
    }
