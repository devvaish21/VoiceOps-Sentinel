import json

with open('sample_transcript.json', 'r') as f:
    data = json.load(f)

# Handle both formats automatically
if isinstance(data, list):
    # Already a list format
    raw_segments = data
else:
    # Dictionary with segments key
    raw_segments = data['segments']

segments = []
for seg in raw_segments:
    segments.append({
        "text": seg['text'],
        "start": seg['start'],
        "end": seg['end']
    })

with open('sample_transcript.json', 'w') as f:
    json.dump(segments, f, indent=2)

print("Done!")
print(f"Total segments: {len(segments)}")

