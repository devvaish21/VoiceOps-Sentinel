from dotenv import load_dotenv
from pyannote.audio import Pipeline
import os
import soundfile as sf
import torch

# Load environment variables from .env file
load_dotenv()

# Initialize a global variable to hold our AI model so we don't have to load it multiple times
_pipeline = None

def get_pipeline():
    global _pipeline
    # If the model hasn't been loaded yet, download and initialize it
    if _pipeline is None:
        _pipeline = Pipeline.from_pretrained(
            'pyannote/speaker-diarization-3.1',
            token=os.getenv('HF_TOKEN')
        )
    return _pipeline

def diarize_audio(audio_path: str) -> list:
    # Fetch the ready ready to use pipeline
    pipeline = get_pipeline()
    # Load the audio file and get its raw and sample rate
    audio_data, sample_rate = sf.read(audio_path)
    # Covert raw audio data to a PyTorch tensor (format needed for the model)
    audio_tensor = torch.tensor(audio_data).float().unsqueeze(0)
    
    # Pass the audio data into the model for speaker diarization
    result = pipeline({
        "waveform": audio_tensor,
        "sample_rate": sample_rate
    })
    
    # Extract the speaker timeline from the result
    annotation = result.speaker_diarization
    # Prepare an empty list to store the final results
    segments = []
    # Loop through every detected spoken sentence to get time segments and speaker labels
    for segment, _, speaker in annotation.itertracks(yield_label=True):
        label = 'Speaker A' if speaker == 'SPEAKER_00' else 'Speaker B'
        # Save timestamps and who spoke into a dictionary
        segments.append({
            'speaker': label,
            'start': round(segment.start, 2),
            'end': round(segment.end, 2)
        })
    # Return the completed list of speaker segments
    return segments

if __name__ == "__main__":
    import json
    result = diarize_audio('test_audio.wav')
    print(json.dumps(result, indent=2))