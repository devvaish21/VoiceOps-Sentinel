"""
sentiment.py — VoiceOps Sentinel | Member 1: AI & Transcription Lead
Analyzes sentiment of a call transcript using Groq (Llama 3).
Returns structured sentiment data for the dashboard.
"""

import os
import re
import json
import time
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a call center sentiment analysis AI.
Given a call transcript, return a JSON object with ONLY these fields:
{
    "overall":            "positive | negative | neutral",
    "score":              0.0,
    "customer_sentiment": "positive | negative | neutral | frustrated | satisfied | angry | calm",
    "agent_sentiment":    "positive | negative | neutral | professional | empathetic | rude | calm",
    "emotional_tone":     "brief description of the emotional arc of the call",
    "escalation_risk":    "low | medium | high"
}
Rules:
- score is a float between -1.0 (very negative) and 1.0 (very positive)
- Be specific about customer and agent sentiment separately
- escalation_risk = high if customer seems unresolved or very upset
Return ONLY valid JSON. No extra text, no markdown, no backticks.
""".strip()

REQUIRED_KEYS        = {"overall", "score", "customer_sentiment", "agent_sentiment",
                         "emotional_tone", "escalation_risk"}
VALID_OVERALL        = {"positive", "negative", "neutral"}
VALID_CUSTOMER_SENT  = {"positive", "negative", "neutral", "frustrated",
                         "satisfied", "angry", "calm"}
VALID_AGENT_SENT     = {"positive", "negative", "neutral", "professional",
                         "empathetic", "rude", "calm"}
VALID_ESCALATION     = {"low", "medium", "high"}

MAX_RETRIES  = 3
RETRY_DELAY  = 2  # seconds


def _strip_markdown_fences(text: str) -> str:
    """Remove ```json ... ``` or ``` ... ``` wrappers Groq sometimes adds."""
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE).strip()


def _call_groq(transcript: str) -> str:
    """Call Groq API with retry on transient errors. Returns raw response string."""
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": f"Transcript:\n\n{transcript}"},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content

        except Exception as e:
            last_error = e
            logger.warning(f"Groq sentiment attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)

    raise RuntimeError(f"Groq sentiment failed after {MAX_RETRIES} attempts: {last_error}") from last_error


def _validate(result: dict) -> dict:
    """Validate required keys, normalize string fields, clamp score."""
    missing = REQUIRED_KEYS - result.keys()
    if missing:
        raise ValueError(f"Groq response missing required keys: {missing}")

    # Normalize and validate enum fields
    for field, valid_set in [
        ("overall",            VALID_OVERALL),
        ("customer_sentiment", VALID_CUSTOMER_SENT),
        ("agent_sentiment",    VALID_AGENT_SENT),
        ("escalation_risk",    VALID_ESCALATION),
    ]:
        value = str(result.get(field, "")).lower().strip()
        if value not in valid_set:
            logger.warning(f"Unexpected value for '{field}': '{value}'. Defaulting to 'neutral'/'low'.")
            result[field] = "neutral" if field != "escalation_risk" else "low"
        else:
            result[field] = value

    # Safe float cast + clamp for score
    try:
        score = float(result["score"])
    except (TypeError, ValueError):
        logger.warning(f"Invalid score value '{result['score']}', defaulting to 0.0")
        score = 0.0
    result["score"] = max(-1.0, min(1.0, score))

    return result


def analyze_sentiment(transcript: str) -> dict:
    """
    Analyze sentiment of a call transcript.

    Args:
        transcript: Plain text transcript from transcriber.py

    Returns:
        {
            "overall":            str,   # positive | negative | neutral
            "score":              float, # -1.0 to 1.0
            "customer_sentiment": str,
            "agent_sentiment":    str,
            "emotional_tone":     str,
            "escalation_risk":    str,   # low | medium | high
        }

    Raises:
        ValueError:   If transcript is empty or response is missing keys.
        RuntimeError: If Groq call fails after retries or returns invalid JSON.
    """
    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty. Cannot analyze sentiment.")

    logger.info("Analyzing sentiment with Groq Llama 3...")

    raw = _call_groq(transcript)
    cleaned = _strip_markdown_fences(raw)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Groq returned invalid JSON after cleaning: {cleaned!r}") from e

    result = _validate(result)

    logger.info(
        f"Sentiment: {result['overall']} "
        f"(score={result['score']}, escalation={result['escalation_risk']})"
    )
    return result


# ── Quick local test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = """
    Agent: Thank you for calling support. How can I help you today?
    Customer: I'm really frustrated. This is the third time I'm calling about the same issue.
    Agent: I sincerely apologize for the inconvenience. Let me look into this right away.
    Customer: I've been waiting for two weeks. This is unacceptable.
    Agent: You're absolutely right and I understand your frustration.
              I'm escalating this to our senior team now.
    Customer: Fine. But if this isn't resolved by tomorrow, I'm cancelling.
    Agent: I completely understand. I'll personally follow up with you by end of day today.
    Customer: Okay. I hope so.
    """

    result = analyze_sentiment(sample)
    print(json.dumps(result, indent=2))