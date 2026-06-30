"""
test_transcriber.py — Unit tests for transcriber.py

transcribe() checks path.exists() before touching Whisper, so every test
that should reach the mocked model needs a REAL temp file on disk (the
content doesn't matter since whisper.load_model is mocked).
"""

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from ai_pipeline.transcriber import transcribe


FAKE_WHISPER_RESULT = {
    "text": "Agent: hello. Customer: I have an issue.",
    "segments": [
        {"id": 0, "start": 0.0, "end": 2.0, "text": "Agent: hello."},
        {"id": 1, "start": 2.0, "end": 5.0, "text": "Customer: I have an issue."},
    ],
    "language": "en",
}


@pytest.fixture
def fake_audio_file():
    """Create a real temp .mp3 file so transcriber's path.exists() check passes."""
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@patch("ai_pipeline.transcriber.whisper.load_model")
def test_transcribe_returns_expected_keys(mock_load_model, fake_audio_file):
    """Output dict must always have these keys for pipeline.py to work."""
    mock_model = MagicMock()
    mock_model.transcribe.return_value = FAKE_WHISPER_RESULT
    mock_load_model.return_value = mock_model

    result = transcribe(fake_audio_file, model_name="base")

    assert "text" in result
    assert "segments" in result
    assert "language" in result
    assert "duration_sec" in result


@patch("ai_pipeline.transcriber.whisper.load_model")
def test_transcribe_uses_correct_model_size(mock_load_model, fake_audio_file):
    mock_model = MagicMock()
    mock_model.transcribe.return_value = FAKE_WHISPER_RESULT
    mock_load_model.return_value = mock_model

    transcribe(fake_audio_file, model_name="small")

    mock_load_model.assert_called_once_with("small")


@patch("ai_pipeline.transcriber.whisper.load_model")
def test_transcribe_raises_on_missing_file(mock_load_model):
    """Should raise FileNotFoundError before even loading the model,
    rather than letting Whisper throw an unclear internal error."""
    with pytest.raises(FileNotFoundError):
        transcribe("/definitely/does/not/exist.mp3")

    mock_load_model.assert_not_called()


@patch("ai_pipeline.transcriber.whisper.load_model")
def test_transcribe_segments_have_timestamps(mock_load_model, fake_audio_file):
    mock_model = MagicMock()
    mock_model.transcribe.return_value = FAKE_WHISPER_RESULT
    mock_load_model.return_value = mock_model

    result = transcribe(fake_audio_file)

    for segment in result["segments"]:
        assert "start" in segment
        assert "end" in segment
        assert "text" in segment