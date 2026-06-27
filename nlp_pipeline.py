from pii_redactor import redact_pii
from action_extractor import extract_action_items
from combine_pipeline import match_speaker_to_text
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

    # Redact PII
    clean_text = redact_pii(full_text)

    # Extract action items
    actions = extract_action_items(clean_text)

    return {
        'labelled_transcript': transcript_segments,
        'redacted_transcript': clean_text,
        'action_items': actions
    }

# Test with sample transcript and diarization
if __name__ == '__main__':

    # Load sample transcript
    with open('sample_transcript.json', 'r') as f:
        transcript = json.load(f)

    # Diarization matching sample timestamps
    diarization = [
        {'speaker': 'Speaker A', 'start': 0.0,    'end': 7.52},
        {'speaker': 'Speaker B', 'start': 8.08,   'end': 15.04},
        {'speaker': 'Speaker A', 'start': 15.04,  'end': 29.2},
        {'speaker': 'Speaker B', 'start': 29.2,   'end': 40.24},
        {'speaker': 'Speaker A', 'start': 40.72,  'end': 62.72},
        {'speaker': 'Speaker B', 'start': 62.72,  'end': 76.56},
        {'speaker': 'Speaker A', 'start': 76.56,  'end': 93.2},
        {'speaker': 'Speaker B', 'start': 93.2,   'end': 101.36},
        {'speaker': 'Speaker A', 'start': 101.36, 'end': 112.8},
    ]

    # Combine speakers with transcript
    segments = match_speaker_to_text(transcript, diarization)

    # Run master pipeline
    result = process_transcript(segments)

    print("=== LABELLED TRANSCRIPT ===")
    for seg in result['labelled_transcript']:
        print(f"{seg['speaker']}: {seg['text'][:60]}...")

    print("\n=== REDACTED TRANSCRIPT ===")
    print(result['redacted_transcript'])

    print("\n=== ACTION ITEMS ===")
    print(json.dumps(result['action_items'], indent=2))