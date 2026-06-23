"""
transcriber.py — VoiceOps Sentinel | Member 1: AI & Transcription Lead
Handles audio file transcription using OpenAI Whisper.

Output format: List of segments with timestamps — compatible with
Ishwarya's diarizer (pyannote needs timestamped chunks, not plain text).
"""

import os
import time
import logging
from pathlib import Path
from typing import Optional

import whisper

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
SUPPORTED_FORMATS = {".mp3", ".mp4", ".wav", ".m4a", ".ogg", ".flac", ".webm"}
DEFAULT_MODEL = "base"   # Options: tiny | base | small | medium | large
                          # Use "base" for dev. Switch to "medium" before demo.

# ── Model loader (cached so it isn't reloaded on every call) ──────────────────
_model_cache: dict = {}

def _load_model(model_name: str = DEFAULT_MODEL) -> whisper.Whisper:
    """Load Whisper model, caching it in memory after first load."""
    if model_name not in _model_cache:
        logger.info(f"Loading Whisper model: {model_name} ...")
        _model_cache[model_name] = whisper.load_model(model_name)
        logger.info(f"Whisper model '{model_name}' loaded successfully.")
    return _model_cache[model_name]


# ── Core transcription function ───────────────────────────────────────────────
def transcribe(
    audio_path: str,
    model_name: str = DEFAULT_MODEL,
    language: Optional[str] = None,
) -> dict:
    """
    Transcribe an audio file using Whisper.

    Args:
        audio_path: Absolute or relative path to the audio file.
        model_name: Whisper model size. Default is "base".
        language:   Force a language (e.g. "en"). None = auto-detect.

    Returns:
        {
            "text":         str,    # Full transcript as plain string
            "segments":     list,   # Timestamped chunks (for Ishwarya's diarizer)
            "language":     str,    # Detected or forced language code
            "duration_sec": float,  # Audio duration in seconds
            "model_used":   str,
        }

    Raises:
        FileNotFoundError: If the audio file does not exist.
        ValueError:        If the file format is not supported.
        RuntimeError:      If Whisper transcription fails.
    """

    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{path.suffix}'. "
            f"Supported: {', '.join(SUPPORTED_FORMATS)}"
        )

    logger.info(f"Transcribing: {path.name} | model={model_name}")
    start_time = time.time()

    model = _load_model(model_name)

    try:
        options = {}
        if language:
            options["language"] = language
        result = model.transcribe(str(path), **options)
    except Exception as e:
        raise RuntimeError(f"Whisper transcription failed: {e}") from e

    elapsed = round(time.time() - start_time, 2)
    logger.info(f"Transcription complete in {elapsed}s.")

    segments = result.get("segments", [])
    duration = round(segments[-1]["end"], 2) if segments else 0.0

    clean_segments = [
        {
            "id":    seg["id"],
            "start": round(seg["start"], 2),
            "end":   round(seg["end"], 2),
            "text":  seg["text"].strip(),
        }
        for seg in segments
    ]

    return {
        "text":         result["text"].strip(),
        "segments":     clean_segments,
        "language":     result.get("language", "unknown"),
        "duration_sec": duration,
        "model_used":   model_name,
    }


# ── Helper: plain text only (for summarizer / sentiment) ─────────────────────
def get_plain_transcript(audio_path: str, **kwargs) -> str:
    """Returns only the plain text transcript. Use in summarizer.py and sentiment.py."""
    return transcribe(audio_path, **kwargs)["text"]


# ── Quick local test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, json

    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <path_to_audio_file>")
        sys.exit(1)

    result = transcribe(sys.argv[1])
    print(f"Language   : {result['language']}")
    print(f"Duration   : {result['duration_sec']}s")
    print(f"\nTranscript :\n{result['text']}")

    out = Path(sys.argv[1]).stem + "_transcript.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to: {out}")