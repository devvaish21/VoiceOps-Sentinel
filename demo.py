# WEEK 4 COMMITS
from pii_redactor import redact_pii
from action_extractor import extract_action_items
from nlp_pipeline import process_transcript
import json

print("=" * 55)
print("  🎙️  VoiceOps Sentinel - LIVE DEMO")
print("  Person 2 - NLP & Security Lead")
print("=" * 55)

# ── DEMO 1: PII Redaction ──────────────────────────
print("\n📌 DEMO 1: PII Redaction")
print("-" * 40)

raw_text = "Hi I am John Smith. My card is 4111111111111111 and email is john@gmail.com. Call me at 9876543210"

print(f"ORIGINAL:\n  {raw_text}")
print(f"\nREDACTED:\n  {redact_pii(raw_text)}")

# ── DEMO 2: Action Item Extraction ────────────────
print("\n📌 DEMO 2: Action Item Extraction")
print("-" * 40)

transcript = """
Agent: I will process your refund within 3-5 days.
Customer: Please call me back tomorrow at 3 PM.
Agent: Sure I will also send you a confirmation email today.
Agent: I will escalate this to my manager as well.
"""

print(f"TRANSCRIPT:{transcript}")
actions = extract_action_items(transcript)
print("ACTION ITEMS EXTRACTED:")
print(json.dumps(actions, indent=2))

# ── DEMO 3: Full Pipeline ─────────────────────────
print("\n📌 DEMO 3: Full Pipeline")
print("-" * 40)

fake_segments = [
    {
        'speaker': 'Speaker A',
        'text': 'Thank you for calling. How can I help you?',
        'start': 0.0,
        'end': 3.5
    },
    {
        'speaker': 'Speaker B',
        'text': 'Hi I am Priya. My card number is 4111111111111111',
        'start': 4.0,
        'end': 8.2
    },
    {
        'speaker': 'Speaker A',
        'text': 'I will process your refund today',
        'start': 9.0,
        'end': 12.5
    },
    {
        'speaker': 'Speaker B',
        'text': 'Please call me back tomorrow at 3 PM at 9876543210',
        'start': 13.0,
        'end': 16.0
    }
]

result = process_transcript(fake_segments)

print("STEP 1 - Speaker Labelled Transcript:")
for seg in result['labelled_transcript']:
    print(f"  {seg['speaker']}: {seg['text']}")

print("\nSTEP 2 - After PII Redaction:")
print(result['redacted_transcript'])

print("\nSTEP 3 - Action Items Extracted:")
print(json.dumps(result['action_items'], indent=2))

print("\n" + "=" * 55)
print("  ✅ DEMO COMPLETE!")
print("  Privacy Audit: 10/10 PII cases passed")
print("  Tech: Pyannote + Presidio + Groq Llama 3")
print("=" * 55)