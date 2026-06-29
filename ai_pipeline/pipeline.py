"""
pipeline.py — VoiceOps Sentinel | Member 1: AI & Transcription Lead
Orchestrates transcription → summarization → sentiment analysis.

This is the ONLY file Tejas (Member 3) needs to import from this module.
Usage from backend:
    from ai_pipeline import run_pipeline
    result = await run_pipeline("/tmp/uploads/call_001.mp3")
"""

import os
import time
import logging
from datetime import datetime, timezone

from .transcriber import transcribe
from .summarizer   import summarize
from .sentiment    import analyze_sentiment

logger = logging.getLogger(__name__)

# Fallback values returned when a non-critical stage fails
_SUMMARY_FALLBACK  = {
    "summary":    None,
    "key_points": [],
    "outcome":    None,
    "call_type":  "unknown",
    "error":      None,   # filled in if stage fails
}
_SENTIMENT_FALLBACK = {
    "overall":            None,
    "score":              None,
    "customer_sentiment": None,
    "agent_sentiment":    None,
    "emotional_tone":     None,
    "escalation_risk":    None,
    "error":              None,  # filled in if stage fails
}


def _validate_audio_path(audio_path: str) -> None:
    """Raise early with a clear message if the file is missing or unsupported."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    supported = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".webm"}
    ext = os.path.splitext(audio_path)[1].lower()
    if ext not in supported:
        raise ValueError(
            f"Unsupported audio format '{ext}'. Supported: {', '.join(sorted(supported))}"
        )


async def run_pipeline(audio_path: str, model: str = "base") -> dict:
    """
    Full AI pipeline: Audio → Transcript → Summary + Sentiment.

    Transcription is critical — failure raises immediately.
    Summarization and sentiment are non-critical — failures return a
    fallback dict with an 'error' key so the pipeline always completes.

    Args:
        audio_path: Path to the uploaded audio file.
        model:      Whisper model size (default: "base").

    Returns:
        {
            "transcript":   str,
            "segments":     list,    # timestamped, for Ishwarya's diarizer
            "language":     str,
            "duration_sec": float,
            "summary":      dict,    # from summarizer (may contain "error" key)
            "sentiment":    dict,    # from sentiment analyzer (may contain "error" key)
            "pipeline_log": dict,    # timing per stage + any stage errors
        }

    Raises:
        FileNotFoundError: If audio file doesn't exist.
        ValueError:        If audio format is unsupported.
        RuntimeError:      If transcription stage fails.
    """

    _validate_audio_path(audio_path)

    logger.info(f"Pipeline started for: {audio_path}")
    pipeline_start = time.time()
    log = {"stage_errors": {}}

    # ── Stage 1: Transcription (critical — raises on failure) ──────────────
    t0 = time.time()
    logger.info("Stage 1/3: Transcription")
    try:
        transcription = transcribe(audio_path, model_name=model)
    except Exception as e:
        raise RuntimeError(f"Transcription failed — pipeline aborted: {e}") from e
    log["transcription_sec"] = round(time.time() - t0, 2)

    transcript_text = transcription["text"]

    # ── Stage 2: Summarization (non-critical — returns fallback on failure) ─
    t0 = time.time()
    logger.info("Stage 2/3: Summarization")
    try:
        summary = summarize(transcript_text)
    except Exception as e:
        logger.error(f"Summarization failed (non-critical): {e}")
        summary = {**_SUMMARY_FALLBACK, "error": str(e)}
        log["stage_errors"]["summarization"] = str(e)
    log["summarization_sec"] = round(time.time() - t0, 2)

    # ── Stage 3: Sentiment Analysis (non-critical — returns fallback on failure)
    t0 = time.time()
    logger.info("Stage 3/3: Sentiment Analysis")
    try:
        sentiment = analyze_sentiment(transcript_text)
    except Exception as e:
        logger.error(f"Sentiment analysis failed (non-critical): {e}")
        sentiment = {**_SENTIMENT_FALLBACK, "error": str(e)}
        log["stage_errors"]["sentiment"] = str(e)
    log["sentiment_sec"] = round(time.time() - t0, 2)

    log["total_sec"]    = round(time.time() - pipeline_start, 2)
    log["completed_at"] = datetime.now(timezone.utc).isoformat()

    # Clean up log if no stage errors occurred
    if not log["stage_errors"]:
        del log["stage_errors"]

    logger.info(f"Pipeline complete in {log['total_sec']}s.")

    # ── Return combined output (Tejas saves this to MongoDB) ───────────────
    return {
        # Transcription
        "transcript":   transcript_text,
        "segments":     transcription["segments"],   # Ishwarya needs this
        "language":     transcription["language"],
        "duration_sec": transcription["duration_sec"],

        # AI outputs
        "summary":      summary,
        "sentiment":    sentiment,

        # Meta
        "pipeline_log": log,
    }


# ── Quick local test (sync wrapper for terminal testing) ──────────────────────
if __name__ == "__main__":
    import sys
    import json
    import asyncio

    if len(sys.argv) < 2:
        print("Usage: python -m ai_pipeline.pipeline <path_to_audio_file>")
        sys.exit(1)

    result = asyncio.run(run_pipeline(sys.argv[1]))

    print("\n===== PIPELINE OUTPUT =====")
    print(f"Language     : {result['language']}")
    print(f"Duration     : {result['duration_sec']}s")
    print(f"Total time   : {result['pipeline_log']['total_sec']}s")
    print(f"\nTranscript   :\n{result['transcript'][:300]}...")
    print(f"\nSummary      :\n{json.dumps(result['summary'], indent=2)}")
    print(f"\nSentiment    :\n{json.dumps(result['sentiment'], indent=2)}")
    print(f"\nPipeline Log :\n{json.dumps(result['pipeline_log'], indent=2)}")