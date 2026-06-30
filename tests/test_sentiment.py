"""
test_sentiment.py — Unit tests for sentiment.py
All Groq API calls are mocked. No real API calls, no internet needed.
"""

import json
import pytest
from unittest.mock import patch, MagicMock

from ai_pipeline.sentiment import analyze_sentiment, _strip_markdown_fences, _validate


def make_mock_response(content: str):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=content))]
    return mock_response


VALID_SENTIMENT_JSON = json.dumps({
    "overall": "negative",
    "score": -0.6,
    "customer_sentiment": "frustrated",
    "agent_sentiment": "empathetic",
    "emotional_tone": "Customer starts upset, agent de-escalates.",
    "escalation_risk": "medium",
})


# ── Tests: empty input ───────────────────────────────────────────────────────

def test_analyze_sentiment_raises_on_empty_transcript():
    with pytest.raises(ValueError):
        analyze_sentiment("")
    with pytest.raises(ValueError):
        analyze_sentiment("   ")


# ── Tests: happy path ────────────────────────────────────────────────────────

@patch("ai_pipeline.sentiment.client")
def test_analyze_sentiment_happy_path(mock_client):
    mock_client.chat.completions.create.return_value = make_mock_response(VALID_SENTIMENT_JSON)

    result = analyze_sentiment("Agent: hi. Customer: this is broken.")

    assert result["overall"] == "negative"
    assert result["score"] == -0.6
    assert result["escalation_risk"] == "medium"


# ── Tests: score clamping ────────────────────────────────────────────────────

@patch("ai_pipeline.sentiment.client")
def test_score_clamped_above_max(mock_client):
    """Groq might return an out-of-range score (e.g. 2.5) — must clamp to 1.0."""
    bad_score_json = json.dumps({**json.loads(VALID_SENTIMENT_JSON), "score": 2.5})
    mock_client.chat.completions.create.return_value = make_mock_response(bad_score_json)

    result = analyze_sentiment("some transcript")
    assert result["score"] == 1.0


@patch("ai_pipeline.sentiment.client")
def test_score_clamped_below_min(mock_client):
    bad_score_json = json.dumps({**json.loads(VALID_SENTIMENT_JSON), "score": -5.0})
    mock_client.chat.completions.create.return_value = make_mock_response(bad_score_json)

    result = analyze_sentiment("some transcript")
    assert result["score"] == -1.0


def test_validate_handles_non_numeric_score():
    """If Groq returns a string or null for score, should default to 0.0 instead of crashing."""
    data = {
        "overall": "neutral", "score": "not a number",
        "customer_sentiment": "calm", "agent_sentiment": "calm",
        "emotional_tone": "flat", "escalation_risk": "low",
    }
    result = _validate(data)
    assert result["score"] == 0.0


# ── Tests: enum validation ───────────────────────────────────────────────────

def test_validate_defaults_invalid_overall():
    data = {
        "overall": "super-duper-happy",  # not a valid value
        "score": 0.5,
        "customer_sentiment": "calm", "agent_sentiment": "calm",
        "emotional_tone": "fine", "escalation_risk": "low",
    }
    result = _validate(data)
    assert result["overall"] == "neutral"


def test_validate_defaults_invalid_escalation_risk():
    data = {
        "overall": "neutral", "score": 0.0,
        "customer_sentiment": "calm", "agent_sentiment": "calm",
        "emotional_tone": "fine",
        "escalation_risk": "extremely high omg",  # not valid
    }
    result = _validate(data)
    assert result["escalation_risk"] == "low"


def test_validate_raises_on_missing_keys():
    incomplete = {"overall": "positive", "score": 0.5}
    with pytest.raises(ValueError, match="missing required keys"):
        _validate(incomplete)


# ── Tests: markdown fence stripping ──────────────────────────────────────────

def test_strip_markdown_fences():
    fenced = f"```json\n{VALID_SENTIMENT_JSON}\n```"
    cleaned = _strip_markdown_fences(fenced)
    assert cleaned == VALID_SENTIMENT_JSON.strip()


# ── Tests: invalid JSON ──────────────────────────────────────────────────────

@patch("ai_pipeline.sentiment.client")
@patch("ai_pipeline.sentiment.time.sleep", return_value=None)
def test_analyze_sentiment_raises_on_invalid_json(mock_sleep, mock_client):
    mock_client.chat.completions.create.return_value = make_mock_response("garbage, not json")

    with pytest.raises(RuntimeError, match="invalid JSON"):
        analyze_sentiment("some transcript")


# ── Tests: retry behavior ────────────────────────────────────────────────────

@patch("ai_pipeline.sentiment.client")
@patch("ai_pipeline.sentiment.time.sleep", return_value=None)
def test_analyze_sentiment_retries_then_succeeds(mock_sleep, mock_client):
    mock_client.chat.completions.create.side_effect = [
        Exception("rate limited"),
        make_mock_response(VALID_SENTIMENT_JSON),
    ]

    result = analyze_sentiment("some transcript")

    assert result["overall"] == "negative"
    assert mock_client.chat.completions.create.call_count == 2


@patch("ai_pipeline.sentiment.client")
@patch("ai_pipeline.sentiment.time.sleep", return_value=None)
def test_analyze_sentiment_raises_after_max_retries(mock_sleep, mock_client):
    mock_client.chat.completions.create.side_effect = Exception("Groq is down")

    with pytest.raises(RuntimeError, match="failed after 3 attempts"):
        analyze_sentiment("some transcript")

    assert mock_client.chat.completions.create.call_count == 3
