import whisper
from pathlib import Path

# Load Whisper model only once
model = whisper.load_model("base")


def transcribe_audio(audio_path: str):
    """
    Transcribes an audio file using OpenAI Whisper.
    """

    if not Path(audio_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    result = model.transcribe(audio_path)

    return {
        "transcript": result["text"].strip(),
        "language": result.get("language", "unknown")
    }