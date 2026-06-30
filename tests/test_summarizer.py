"""
test_summarizer.py — Unit tests for summarizer.py
All Groq API calls are mocked. No real API calls, no internet needed.
"""

import json
import pytest
from unittest.mock import patch, MagicMock

from ai_pipeline.summarizer import summarize, _strip_markdown_fences, _validate


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_mock_response(content: str):
    """Build a fake Groq response object matching client.chat.completions.create() shape."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=content))]
    return mock_response


VALID_SUMMARY_JSON = json.dumps({
    "summary": "Customer reported a billing issue and was refunded.",
    "key_points": ["Duplicate charge", "Refund processed", "3-5 day wait"],
    "outcome": "Refund issued",
    "call_type": "support",
})


# ── Tests: empty input ───────────────────────────────────────────────────────

def test_summarize_raises_on_empty_transcript():
    """Empty or whitespace-only transcript should raise ValueError before any API call."""
    with pytest.raises(ValueError):
        summarize("")
    with pytest.raises(ValueError):
        summarize("   ")


# ── Tests: happy path ────────────────────────────────────────────────────────

@patch("ai_pipeline.summarizer.client")
def test_summarize_happy_path(mock_client):
    """Valid transcript + valid Groq JSON response → correctly parsed dict."""
    mock_client.chat.completions.create.return_value = make_mock_response(VALID_SUMMARY_JSON)

    result = summarize("Agent: hello. Customer: I have an issue.")

    assert result["summary"] == "Customer reported a billing issue and was refunded."
    assert result["key_points"] == ["Duplicate charge", "Refund processed", "3-5 day wait"]
    assert result["call_type"] == "support"
    mock_client.chat.completions.create.assert_called_once()


# ── Tests: markdown fence stripping ──────────────────────────────────────────

def test_strip_markdown_fences_removes_json_fence():
    fenced = f"```json\n{VALID_SUMMARY_JSON}\n```"
    cleaned = _strip_markdown_fences(fenced)
    assert cleaned == VALID_SUMMARY_JSON.strip()


def test_strip_markdown_fences_removes_plain_fence():
    fenced = f"```\n{VALID_SUMMARY_JSON}\n```"
    cleaned = _strip_markdown_fences(fenced)
    assert cleaned == VALID_SUMMARY_JSON.strip()


def test_strip_markdown_fences_noop_on_clean_json():
    cleaned = _strip_markdown_fences(VALID_SUMMARY_JSON)
    assert cleaned == VALID_SUMMARY_JSON.strip()


@patch("ai_pipeline.summarizer.client")
def test_summarize_handles_fenced_response(mock_client):
    """Groq sometimes wraps JSON in markdown fences despite instructions — should still parse."""
    fenced = f"```json\n{VALID_SUMMARY_JSON}\n```"
    mock_client.chat.completions.create.return_value = make_mock_response(fenced)

    result = summarize("some transcript")

    assert result["call_type"] == "support"


# ── Tests: invalid JSON from Groq ────────────────────────────────────────────

@patch("ai_pipeline.summarizer.client")
@patch("ai_pipeline.summarizer.time.sleep", return_value=None)  # skip real retry delays
def test_summarize_raises_on_invalid_json(mock_sleep, mock_client):
    """Non-JSON garbage from Groq should raise RuntimeError, not crash with a raw traceback."""
    mock_client.chat.completions.create.return_value = make_mock_response("not valid json at all")

    with pytest.raises(RuntimeError, match="invalid JSON"):
        summarize("some transcript")


# ── Tests: missing required keys ─────────────────────────────────────────────

def test_validate_raises_on_missing_keys():
    incomplete = {"summary": "x", "key_points": []}  # missing outcome, call_type
    with pytest.raises(ValueError, match="missing required keys"):
        _validate(incomplete)


def test_validate_defaults_unknown_call_type():
    """Unexpected call_type values should be normalized to 'other', not raise."""
    data = {
        "summary": "x", "key_points": [], "outcome": "y",
        "call_type": "totally_made_up_type",
    }
    result = _validate(data)
    assert result["call_type"] == "other"


def test_validate_raises_if_key_points_not_list():
    data = {
        "summary": "x", "key_points": "not a list", "outcome": "y", "call_type": "support",
    }
    with pytest.raises(ValueError, match="key_points"):
        _validate(data)


# ── Tests: retry behavior ────────────────────────────────────────────────────

@patch("ai_pipeline.summarizer.client")
@patch("ai_pipeline.summarizer.time.sleep", return_value=None)
def test_summarize_retries_on_transient_failure(mock_sleep, mock_client):
    """First 2 calls fail (simulating network blip), 3rd succeeds — should NOT raise."""
    mock_client.chat.completions.create.side_effect = [
        Exception("connection reset"),
        Exception("timeout"),
        make_mock_response(VALID_SUMMARY_JSON),
    ]

    result = summarize("some transcript")

    assert result["call_type"] == "support"
    assert mock_client.chat.completions.create.call_count == 3


@patch("ai_pipeline.summarizer.client")
@patch("ai_pipeline.summarizer.time.sleep", return_value=None)
def test_summarize_raises_after_max_retries_exhausted(mock_sleep, mock_client):
    """All 3 attempts fail → should raise RuntimeError, not retry forever."""
    mock_client.chat.completions.create.side_effect = Exception("Groq is down")

    with pytest.raises(RuntimeError, match="failed after 3 attempts"):
        summarize("some transcript")

    assert mock_client.chat.completions.create.call_count == 3
