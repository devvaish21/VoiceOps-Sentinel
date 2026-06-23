from dotenv import load_dotenv
from pyannote.audio import Pipeline
import os
import soundfile as sf
import torch

load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')

print('Loading Pyannote...')
pipeline = Pipeline.from_pretrained(
    'pyannote/speaker-diarization-3.1',
    token=HF_TOKEN
)

print('Running diarization...')
audio_data, sample_rate = sf.read('test_audio.wav')
audio_tensor = torch.tensor(audio_data).float().unsqueeze(0)

diarization = pipeline({
    "waveform": audio_tensor,
    "sample_rate": sample_rate
})

print('RESULTS:')
annotation = diarization.speaker_diarization
for segment, track, speaker in annotation.itertracks(yield_label=True):
    print(f'  {speaker}: {segment.start:.2f}s to {segment.end:.2f}s')