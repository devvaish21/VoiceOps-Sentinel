from dotenv import load_dotenv
from pyannote.audio import Pipeline
import os
import soundfile as sf
import torch

load_dotenv()

_pipeline = None

def get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline.from_pretrained(
            'pyannote/speaker-diarization-3.1',
            token=os.getenv('HF_TOKEN')
        )
    return _pipeline

def diarize_audio(audio_path: str) -> list:
    pipeline = get_pipeline()
    audio_data, sample_rate = sf.read(audio_path)
    audio_tensor = torch.tensor(audio_data).float().unsqueeze(0)
    
    result = pipeline({
        "waveform": audio_tensor,
        "sample_rate": sample_rate
    })
    
    annotation = result.speaker_diarization
    segments = []
    for segment, _, speaker in annotation.itertracks(yield_label=True):
        label = 'Speaker A' if speaker == 'SPEAKER_00' else 'Speaker B'
        segments.append({
            'speaker': label,
            'start': round(segment.start, 2),
            'end': round(segment.end, 2)
        })
    return segments

if __name__ == "__main__":
    import json
    result = diarize_audio('test_audio.wav')
    print(json.dumps(result, indent=2))
