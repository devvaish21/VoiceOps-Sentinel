"""
test_pipeline.py — Unit tests for pipeline.py
transcribe(), summarize(), and analyze_sentiment() are all mocked.
This tests ORCHESTRATION logic only: does the pipeline call stages correctly,
does it fail/succeed in the right cases, does it return the right shape.
"""

import pytest
import tempfile
import os
from unittest.mock import patch

from ai_pipeline.pipeline import run_pipeline, _validate_audio_path


# ── Helpers ──────────────────────────────────────────────────────────────────

FAKE_TRANSCRIPTION = {
    "text": "Agent: hello. Customer: I have an issue.",
    "segments": [{"start": 0.0, "end": 2.0, "text": "Agent: hello."}],
    "language": "en",
    "duration_sec": 12.5,
}

FAKE_SUMMARY = {
    "summary": "Customer had an issue, agent resolved it.",
    "key_points": ["Issue raised", "Resolved"],
    "outcome": "Resolved",
    "call_type": "support",
}

FAKE_SENTIMENT = {
    "overall": "positive",
    "score": 0.4,
    "customer_sentiment": "satisfied",
    "agent_sentiment": "professional",
    "emotional_tone": "Calm and resolved.",
    "escalation_risk": "low",
}


@pytest.fixture
def fake_audio_file():
    """Create a real temp .mp3 file so path validation passes."""
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


# ── Tests: audio path validation ─────────────────────────────────────────────

def test_validate_audio_path_raises_if_missing():
    with pytest.raises(FileNotFoundError):
        _validate_audio_path("/nonexistent/path/call.mp3")


def test_validate_audio_path_raises_on_unsupported_extension(fake_audio_file):
    bad_path = fake_audio_file.replace(".mp3", ".exe")
    os.rename(fake_audio_file, bad_path)
    try:
        with pytest.raises(ValueError, match="Unsupported audio format"):
            _validate_audio_path(bad_path)
    finally:
        # Clean up the renamed file ourselves and recreate the original path
        # so the fixture's own teardown (os.remove(fake_audio_file)) doesn't error.
        if os.path.exists(bad_path):
            os.remove(bad_path)
        open(fake_audio_file, "w").close()


def test_validate_audio_path_passes_for_supported_format(fake_audio_file):
    _validate_audio_path(fake_audio_file)  # should not raise


# ── Tests: happy path ────────────────────────────────────────────────────────

@pytest.mark.asyncio
@patch("ai_pipeline.pipeline.analyze_sentiment")
@patch("ai_pipeline.pipeline.summarize")
@patch("ai_pipeline.pipeline.transcribe")
async def test_run_pipeline_happy_path(mock_transcribe, mock_summarize, mock_sentiment, fake_audio_file):
    mock_transcribe.return_value = FAKE_TRANSCRIPTION
    mock_summarize.return_value = FAKE_SUMMARY
    mock_sentiment.return_value = FAKE_SENTIMENT

    result = await run_pipeline(fake_audio_file)

    assert result["transcript"] == FAKE_TRANSCRIPTION["text"]
    assert result["segments"] == FAKE_TRANSCRIPTION["segments"]
    assert result["summary"] == FAKE_SUMMARY
    assert result["sentiment"] == FAKE_SENTIMENT
    assert "total_sec" in result["pipeline_log"]
    assert "stage_errors" not in result["pipeline_log"]  # no errors occurred


# ── Tests: critical failure (transcription) ──────────────────────────────────

@pytest.mark.asyncio
@patch("ai_pipeline.pipeline.transcribe")
async def test_run_pipeline_raises_if_transcription_fails(mock_transcribe, fake_audio_file):
    """Transcription is critical — pipeline must abort, not return partial results."""
    mock_transcribe.side_effect = Exception("Whisper crashed")

    with pytest.raises(RuntimeError, match="Transcription failed"):
        await run_pipeline(fake_audio_file)


# ── Tests: non-critical failures (summary / sentiment) ───────────────────────

@pytest.mark.asyncio
@patch("ai_pipeline.pipeline.analyze_sentiment")
@patch("ai_pipeline.pipeline.summarize")
@patch("ai_pipeline.pipeline.transcribe")
async def test_run_pipeline_continues_if_summary_fails(
    mock_transcribe, mock_summarize, mock_sentiment, fake_audio_file
):
    """If summarizer crashes, pipeline should still return transcript + sentiment,
    with summary containing an 'error' key instead of raising."""
    mock_transcribe.return_value = FAKE_TRANSCRIPTION
    mock_summarize.side_effect = RuntimeError("Groq summarization failed after 3 attempts")
    mock_sentiment.return_value = FAKE_SENTIMENT

    result = await run_pipeline(fake_audio_file)

    assert result["transcript"] == FAKE_TRANSCRIPTION["text"]
    assert result["summary"]["error"] is not None
    assert result["sentiment"] == FAKE_SENTIMENT  # sentiment still succeeded
    assert "summarization" in result["pipeline_log"]["stage_errors"]


@pytest.mark.asyncio
@patch("ai_pipeline.pipeline.analyze_sentiment")
@patch("ai_pipeline.pipeline.summarize")
@patch("ai_pipeline.pipeline.transcribe")
async def test_run_pipeline_continues_if_sentiment_fails(
    mock_transcribe, mock_summarize, mock_sentiment, fake_audio_file
):
    mock_transcribe.return_value = FAKE_TRANSCRIPTION
    mock_summarize.return_value = FAKE_SUMMARY
    mock_sentiment.side_effect = RuntimeError("Groq sentiment failed after 3 attempts")

    result = await run_pipeline(fake_audio_file)

    assert result["summary"] == FAKE_SUMMARY  # summary still succeeded
    assert result["sentiment"]["error"] is not None
    assert "sentiment" in result["pipeline_log"]["stage_errors"]


@pytest.mark.asyncio
@patch("ai_pipeline.pipeline.analyze_sentiment")
@patch("ai_pipeline.pipeline.summarize")
@patch("ai_pipeline.pipeline.transcribe")
async def test_run_pipeline_continues_if_both_summary_and_sentiment_fail(
    mock_transcribe, mock_summarize, mock_sentiment, fake_audio_file
):
    """Worst case: both non-critical stages fail. Pipeline should still return
    a usable result with the transcript intact."""
    mock_transcribe.return_value = FAKE_TRANSCRIPTION
    mock_summarize.side_effect = RuntimeError("summary boom")
    mock_sentiment.side_effect = RuntimeError("sentiment boom")

    result = await run_pipeline(fake_audio_file)

    assert result["transcript"] == FAKE_TRANSCRIPTION["text"]
    assert result["summary"]["error"] is not None
    assert result["sentiment"]["error"] is not None
    assert len(result["pipeline_log"]["stage_errors"]) == 2


# ── Tests: pipeline_log timing fields ─────────────────────────────────────────

@pytest.mark.asyncio
@patch("ai_pipeline.pipeline.analyze_sentiment")
@patch("ai_pipeline.pipeline.summarize")
@patch("ai_pipeline.pipeline.transcribe")
async def test_pipeline_log_contains_all_timing_fields(
    mock_transcribe, mock_summarize, mock_sentiment, fake_audio_file
):
    mock_transcribe.return_value = FAKE_TRANSCRIPTION
    mock_summarize.return_value = FAKE_SUMMARY
    mock_sentiment.return_value = FAKE_SENTIMENT

    result = await run_pipeline(fake_audio_file)
    log = result["pipeline_log"]

    for key in ["transcription_sec", "summarization_sec", "sentiment_sec", "total_sec", "completed_at"]:
        assert key in log