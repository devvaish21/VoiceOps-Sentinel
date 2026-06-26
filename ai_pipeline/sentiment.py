"""
sentiment.py — VoiceOps Sentinel | Member 1: AI & Transcription Lead
Analyzes sentiment of a call transcript using GPT-4.
Returns structured sentiment data for the dashboard.
"""

import os
import json
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
    "overall":           "positive | negative | neutral",
    "score":             0.0,
    "customer_sentiment": "positive | negative | neutral | frustrated | satisfied | angry | calm",
    "agent_sentiment":   "positive | negative | neutral | professional | empathetic | rude | calm",
    "emotional_tone":    "brief description of the emotional arc of the call",
    "escalation_risk":   "low | medium | high"
}
Rules:
- score is a float between -1.0 (very negative) and 1.0 (very positive)
- Be specific about customer and agent sentiment separately
- escalation_risk = high if customer seems unresolved or very upset
Return ONLY valid JSON. No extra text, no markdown, no backticks.
""".strip()


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
        ValueError:   If transcript is empty.
        RuntimeError: If GPT call fails or returns invalid JSON.
    """
    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty. Cannot analyze sentiment.")

    logger.info("Analyzing sentiment with GPT-4...")

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
    except Exception as e:
        raise RuntimeError(f"GPT sentiment analysis failed: {e}") from e

    raw = response.choices[0].message.content

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"GPT returned invalid JSON: {raw}") from e

    # Clamp score to valid range just in case
    result["score"] = max(-1.0, min(1.0, float(result.get("score", 0.0))))

    logger.info(
        f"Sentiment: {result.get('overall')} "
        f"(score={result.get('score')}, escalation={result.get('escalation_risk')})"
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