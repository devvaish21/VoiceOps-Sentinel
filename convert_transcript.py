import json
# Convert the transcript to list format if it is dictionary with segments key
with open('sample_transcript.json', 'r') as f:
    data = json.load(f)

# Handle both formats automatically
if isinstance(data, list):
    # Already a list format
    raw_segments = data
else:
    # Dictionary with segments key
    raw_segments = data['segments']

# Convert list of segments text to list of dictionaries with text, start, and end keys
segments = []
for seg in raw_segments:
    segments.append({
        "text": seg['text'],
        "start": seg['start'],
        "end": seg['end']
    })
# Save the segments to a new JSON file
with open('sample_transcript.json', 'w') as f:
    json.dump(segments, f, indent=2)

print("Done!")
print(f"Total segments: {len(segments)}")
