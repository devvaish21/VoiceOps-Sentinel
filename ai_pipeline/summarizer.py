"""
summarizer.py — VoiceOps Sentinel | Member 1: AI & Transcription Lead
Generates a structured summary of a call transcript using Groq (Llama 3).
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
You are an AI assistant that analyzes call transcripts.
Given a transcript, return a JSON object with ONLY these fields:
{
    "summary":      "3-5 sentence overview of the entire call",
    "key_points":   ["point 1", "point 2", "point 3"],
    "outcome":      "What was resolved or decided at the end of the call",
    "call_type":    "support | sales | internal | complaint | other"
}
Return ONLY valid JSON. No extra text, no markdown, no backticks.
""".strip()

REQUIRED_KEYS = {"summary", "key_points", "outcome", "call_type"}
VALID_CALL_TYPES = {"support", "sales", "internal", "complaint", "other"}

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


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
                temperature=0.3,
            )
            return response.choices[0].message.content

        except Exception as e:
            last_error = e
            logger.warning(f"Groq summarization attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)  # exponential-ish backoff

    raise RuntimeError(f"Groq summarization failed after {MAX_RETRIES} attempts: {last_error}") from last_error


def _validate(result: dict) -> dict:
    """Check required keys exist and normalize call_type."""
    missing = REQUIRED_KEYS - result.keys()
    if missing:
        raise ValueError(f"Groq response missing required keys: {missing}")

    if not isinstance(result["key_points"], list):
        raise ValueError(f"'key_points' must be a list, got: {type(result['key_points'])}")

    call_type = result.get("call_type", "").lower().strip()
    if call_type not in VALID_CALL_TYPES:
        logger.warning(f"Unexpected call_type '{call_type}', defaulting to 'other'.")
        result["call_type"] = "other"
    else:
        result["call_type"] = call_type

    return result


def summarize(transcript: str) -> dict:
    """
    Summarize a call transcript using Groq Llama 3.

    Args:
        transcript: Plain text transcript from transcriber.py

    Returns:
        {
            "summary":    str,   # 3-5 sentence overview
            "key_points": list,  # bullet points
            "outcome":    str,   # resolution
            "call_type":  str,   # support | sales | internal | complaint | other
        }

    Raises:
        ValueError:   If transcript is empty or response is missing keys.
        RuntimeError: If Groq call fails after retries or returns invalid JSON.
    """
    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty. Cannot summarize.")

    logger.info("Generating call summary with Groq Llama 3...")

    raw = _call_groq(transcript)
    cleaned = _strip_markdown_fences(raw)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Groq returned invalid JSON after cleaning: {cleaned!r}") from e

    result = _validate(result)

    logger.info(f"Summary generated. Call type: {result['call_type']}")
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = json.load(f)
        transcript = data.get("text", "")
    else:
        transcript = """
        Agent: Thank you for calling support. How can I help you today?
        Customer: Hi, I've been charged twice for my subscription this month.
        Agent: I'm sorry to hear that. Let me pull up your account.
        Agent: Yes, I can see the duplicate charge. I'll process a refund immediately.
        Customer: How long will that take?
        Agent: 3 to 5 business days. You'll get a confirmation email shortly.
        Customer: Great, thank you so much.
        Agent: You're welcome. Is there anything else I can help you with?
        Customer: No, that's all. Goodbye.
        """

    result = summarize(transcript)
    print(json.dumps(result, indent=2))