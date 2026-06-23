"""
summarizer.py — VoiceOps Sentinel | Member 1: AI & Transcription Lead
Generates a structured summary of a call transcript using GPT-4.
"""

import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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


def summarize(transcript: str) -> dict:
    """
    Generate a structured summary from a transcript string.

    Args:
        transcript: Plain text transcript from transcriber.py

    Returns:
        {
            "summary":    str,
            "key_points": list[str],
            "outcome":    str,
            "call_type":  str,
        }

    Raises:
        ValueError:   If transcript is empty.
        RuntimeError: If GPT call fails or returns invalid JSON.
    """
    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty. Cannot summarize.")

    logger.info("Generating call summary with GPT-4...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Transcript:\n\n{transcript}"},
            ],
            temperature=0.3,        # Low temp = consistent, factual output
            response_format={"type": "json_object"},  # GPT-4o JSON mode
        )
    except Exception as e:
        raise RuntimeError(f"GPT summarization failed: {e}") from e

    raw = response.choices[0].message.content

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"GPT returned invalid JSON: {raw}") from e

    logger.info(f"Summary generated. Call type: {result.get('call_type', 'unknown')}")
    return result


# ── Quick local test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = """
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

    result = summarize(sample)
    print(json.dumps(result, indent=2))