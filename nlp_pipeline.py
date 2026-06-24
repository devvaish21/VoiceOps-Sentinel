from pii_redactor import redact_pii
from action_extractor import extract_action_items
import json

def process_transcript(transcript_segments: list) -> dict:
    """
    MASTER FUNCTION
    Takes labelled transcript segments from combine_pipeline
    Returns complete NLP analysis
    """
    # Build full transcript text
    full_text = '\n'.join(
        f"{seg['speaker']}: {seg['text']}"
        for seg in transcript_segments
    )

    # Step 1 - Redact PII
    clean_text = redact_pii(full_text)

    # Step 2 - Extract action items
    actions = extract_action_items(clean_text)

    return {
        'labelled_transcript': transcript_segments,
        'redacted_transcript': clean_text,
        'action_items': actions
    }

# Test it
if __name__ == '__main__':
    # Fake labelled segments (from combine_pipeline)
    fake_segments = [
        {
            'speaker': 'Speaker A',
            'text': 'Hello how can I help you today?',
            'start': 0.0,
            'end': 3.5
        },
        {
            'speaker': 'Speaker B',
            'text': 'Hi my name is John. My number is 9876543210',
            'start': 4.0,
            'end': 8.2
        },
        {
            'speaker': 'Speaker A',
            'text': 'Sure I will process your refund today',
            'start': 9.0,
            'end': 12.5
        },
        {
            'speaker': 'Speaker B',
            'text': 'Please call me back tomorrow at 3 PM',
            'start': 13.0,
            'end': 16.0
        }
    ]

    result = process_transcript(fake_segments)

    print("=== LABELLED TRANSCRIPT ===")
    for seg in result['labelled_transcript']:
        print(f"{seg['speaker']}: {seg['text']}")

    print("\n=== REDACTED TRANSCRIPT ===")
    print(result['redacted_transcript'])

    print("\n=== ACTION ITEMS ===")
    print(json.dumps(result['action_items'], indent=2))
