import json

def match_speaker_to_text(transcript_segments, diarization_segments):
    # Initialize an empty list to store the final result
    result = []
    # Loop through each text segment from the transcription (Whisper/JSON) data
    for t_seg in transcript_segments:
        # Calculate the exact midpoint time of the current spoken segment
        t_mid = (t_seg['start'] + t_seg['end']) / 2
        speaker = 'Unknown'
        # Look through  the AI diarization segments to find the matching speaker
        for d_seg in diarization_segments:
            if d_seg['start'] <= t_mid <= d_seg['end']:
                speaker = d_seg['speaker']
                break
        # Append the matched segment to the result
        result.append({
            'speaker': speaker,
            'text': t_seg['text'],
            'start': t_seg['start'],
            'end': t_seg['end']
        })
    return result

if __name__ == '__main__':
    with open('sample_transcript.json', 'r') as f:
        transcript = json.load(f)

    # Mock diarization data for testing purposes
    diarization = [
        {'speaker': 'Speaker A', 'start': 0.0,   'end': 7.52},
        {'speaker': 'Speaker B', 'start': 8.08,  'end': 15.04},
        {'speaker': 'Speaker A', 'start': 15.04, 'end': 29.2},
        {'speaker': 'Speaker B', 'start': 29.2,  'end': 40.24},
        {'speaker': 'Speaker A', 'start': 40.72, 'end': 62.72},
        {'speaker': 'Speaker B', 'start': 62.72, 'end': 76.56},
        {'speaker': 'Speaker A', 'start': 76.56, 'end': 93.2},
        {'speaker': 'Speaker B', 'start': 93.2,  'end': 101.36},
        {'speaker': 'Speaker A', 'start': 101.36,'end': 112.8},
    ]

    # Call the function to match speakers to text segments
    result = match_speaker_to_text(transcript, diarization)
    # Print the final combined JSON out clearly formatted for readability
    print(json.dumps(result, indent=2))