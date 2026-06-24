import json

def match_speaker_to_text(transcript_segments, diarization_segments):
    result = []
    for t_seg in transcript_segments:
        t_mid = (t_seg['start'] + t_seg['end']) / 2
        speaker = 'Unknown'
        for d_seg in diarization_segments:
            if d_seg['start'] <= t_mid <= d_seg['end']:
                speaker = d_seg['speaker']
                break
        result.append({
            'speaker': speaker,
            'text': t_seg['text'],
            'start': t_seg['start'],
            'end': t_seg['end']
        })
    return result

if __name__ == '__main__':
    # ALL these lines must be INSIDE if block!
    with open('sample_transcript.json', 'r') as f:
        transcript = json.load(f)

    diarization = [
        {'speaker': 'Speaker A', 'start': 0.03, 'end': 3.6},
        {'speaker': 'Speaker B', 'start': 4.0, 'end': 8.5},
        {'speaker': 'Speaker A', 'start': 9.0, 'end': 13.0},
        {'speaker': 'Speaker B', 'start': 13.0, 'end': 16.5},
        {'speaker': 'Speaker A', 'start': 80.0, 'end': 87.0},
    ]

    # This line must also be INSIDE if block!
    result = match_speaker_to_text(transcript, diarization)
    print(json.dumps(result, indent=2))  