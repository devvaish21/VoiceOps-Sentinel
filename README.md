[README (5).md](https://github.com/user-attachments/files/30111576/README.5.md)
# VoiceOps Sentinel — AI Pipeline Module
**Branch:** `ai-pipeline` | **Member 1:** Vaishnavi (AI & Transcription Lead)

This module takes a raw audio file of a customer support call and returns a structured transcript, summary, and sentiment report — in one function call.

---

## How It Works

```
Audio File → Transcription (Whisper) → Summarization (Groq) → Sentiment Analysis (Groq) → JSON Output
```

---

## Folder Structure

```
ai_pipeline/
├── pipeline.py        # Main entry point — runs all 3 stages
├── transcriber.py     # Converts audio to text using Whisper
├── summarizer.py      # Summarizes the transcript using Groq Llama 3
├── sentiment.py       # Analyzes sentiment using Groq Llama 3
├── generate_sample.py # Generates a test audio file
└── __init__.py        # Exports run_pipeline

tests/                 # 37 unit tests, all passing
```

---

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Install ffmpeg** (required by Whisper)
- Windows: Download from ffmpeg.org, add `ffmpeg/bin` to PATH
- Mac: `brew install ffmpeg`

**3. Set up your API key**
```bash
cp .env.example .env
# Add your GROQ_API_KEY inside .env
```
Get a free Groq API key at [console.groq.com](https://console.groq.com).

---

## For Tejas — How to Use This

```python
from ai_pipeline import run_pipeline

result = await run_pipeline("/path/to/call.mp3")
```

The result dict contains everything you need to save to MongoDB:

```python
{
    "transcript":   str,       # Full text of the call
    "segments":     list,      # Timestamped chunks (needed by Ishwarya)
    "language":     str,       # e.g. "en"
    "duration_sec": float,     # Audio length in seconds

    "summary": {
        "summary":    str,     # 3-5 sentence overview
        "key_points": list,    # Main points from the call
        "outcome":    str,     # How the call ended
        "call_type":  str,     # support | sales | complaint | other
    },

    "sentiment": {
        "overall":            str,   # positive | negative | neutral
        "score":              float, # -1.0 to 1.0
        "customer_sentiment": str,   # e.g. frustrated | satisfied | angry
        "agent_sentiment":    str,   # e.g. empathetic | professional
        "emotional_tone":     str,   # Short description of the call's mood
        "escalation_risk":    str,   # low | medium | high
    },

    "pipeline_log": {
        "total_sec":    float,  # How long the pipeline took
        "completed_at": str,    # UTC timestamp
    }
}
```

**Supported formats:** `.mp3` `.wav` `.m4a` `.flac` `.ogg` `.webm`

---

## For Ishwarya — Segments Format

The `segments` field is a list of timestamped chunks from Whisper:

```python
[
    {"id": 0, "start": 0.0,  "end": 7.5,  "text": "Agent. Thank you for calling..."},
    {"id": 1, "start": 8.0,  "end": 15.0, "text": "Customer. I have a problem..."},
    ...
]
```

See `sample_call_transcript.json` for a full real example (15 segments, 112.8s).

---

## Running Locally

**Generate test audio:**
```bash
python ai_pipeline/generate_sample.py
```

**Run the full pipeline:**
```bash
python -m ai_pipeline.pipeline sample_call.mp3
```

**Run unit tests:**
```bash
python -m pytest tests/ -v
```

---

## Tech Stack

| | Technology |
|---|---|
| Transcription | OpenAI Whisper (base model) |
| Summarization + Sentiment | Groq API — Llama 3.3 70B |
| Testing | pytest + unittest.mock |

> Groq is used instead of OpenAI because it's free tier — no billing needed. Llama 3.3 70B handles structured JSON tasks well.

---

*VoiceOps Sentinel · Team: Vaishnavi (AI & Transcription) · Ishwarya (NLP & Security) · Tejas (Backend & Frontend)*
