import os
import torch
import whisperx
from whisperx.diarize import DiarizationPipeline, assign_word_speakers
from dotenv import load_dotenv
from app.graph.state import State

load_dotenv()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
HF_TOKEN = os.getenv("HF_TOKEN")

model = whisperx.load_model(
    "base",
    DEVICE,
    compute_type="float16" if DEVICE == "cuda" else "int8"
)


def transcription_agent(state: State) -> dict:
    message = state["messages"][-1]
    audio_path = message.content if hasattr(message, "content") else message["content"]

    # Step 1: Transcribe
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=4)
    detected_language = result["language"]

    # Step 2: Word-level alignment
    align_model, metadata = whisperx.load_align_model(
        language_code=detected_language, device=DEVICE
    )
    aligned = whisperx.align(
        result["segments"], align_model, metadata, audio, DEVICE
    )

    # Step 3: Speaker diarization
    diarize_model = DiarizationPipeline(
        model_name="pyannote/speaker-diarization-3.1", 
        token=HF_TOKEN,
        device=DEVICE
        )
        
    diarize_segments = diarize_model(audio)

    # Step 4: Assign speakers to words
    result_with_speakers = assign_word_speakers(diarize_segments, aligned)

    # Step 5: Format output
    lines = []
    for seg in result_with_speakers["segments"]:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        speaker = seg.get("speaker", "UNKNOWN")
        start_fmt = f"{int(start//60):02d}:{start%60:05.2f}"
        end_fmt = f"{int(end//60):02d}:{end%60:05.2f}"
        lines.append(f"[{start_fmt} - {end_fmt}]  {speaker}: {text}")

    output = f"Language: {detected_language}\n\n" + "\n".join(lines)

    return {
        "messages": [{"role": "assistant", "content": output}],
        "route_to": "end"
    }
