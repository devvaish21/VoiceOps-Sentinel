"""
pipeline.py — VoiceOps Sentinel | Member 1: AI & Transcription Lead
Orchestrates transcription → summarization → sentiment analysis.

This is the ONLY file Tejas (Member 3) needs to import from this module.
Usage from backend:
    from ai_pipeline import run_pipeline
    result = await run_pipeline("/tmp/uploads/call_001.mp3")
"""

import time
import logging
from datetime import datetime, timezone

from .transcriber import transcribe
from .summarizer   import summarize
from .sentiment    import analyze_sentiment

logger = logging.getLogger(__name__)


async def run_pipeline(audio_path: str, model: str = "base") -> dict:
    """
    Full AI pipeline: Audio → Transcript → Summary + Sentiment.

    Args:
        audio_path: Path to the uploaded audio file.
        model:      Whisper model size (default: "base").

    Returns:
        {
            "transcript":  str,
            "segments":    list,    # timestamped, for Ishwarya's diarizer
            "language":    str,
            "duration_sec": float,
            "summary":     dict,    # from summarizer
            "sentiment":   dict,    # from sentiment analyzer
            "pipeline_log": dict,   # timing per stage (for MongoDB + review)
        }

    Raises:
        FileNotFoundError: If audio file doesn't exist.
        RuntimeError:      If any stage fails.
    """

    logger.info(f"Pipeline started for: {audio_path}")
    pipeline_start = time.time()
    log = {}

    # ── Stage 1: Transcription ─────────────────────────────────────────────
    t0 = time.time()
    logger.info("Stage 1/3: Transcription")
    transcription = transcribe(audio_path, model_name=model)
    log["transcription_sec"] = round(time.time() - t0, 2)

    transcript_text = transcription["text"]

    # ── Stage 2: Summarization ─────────────────────────────────────────────
    t0 = time.time()
    logger.info("Stage 2/3: Summarization")
    summary = summarize(transcript_text)
    log["summarization_sec"] = round(time.time() - t0, 2)

    # ── Stage 3: Sentiment Analysis ────────────────────────────────────────
    t0 = time.time()
    logger.info("Stage 3/3: Sentiment Analysis")
    sentiment = analyze_sentiment(transcript_text)
    log["sentiment_sec"] = round(time.time() - t0, 2)

    log["total_sec"]   = round(time.time() - pipeline_start, 2)
    log["completed_at"] = datetime.now(timezone.utc).isoformat()

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
        print("Usage: python pipeline.py <path_to_audio_file>")
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