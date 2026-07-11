# VoiceOps Sentinel - Person 2 (NLP & Security)

## My Role
NLP & Security Lead

## What I Built
- Speaker Diarization (Pyannote)
- PII Redaction (Microsoft Presidio)  
- Action Item Extraction (Groq Llama 3)

## My Functions
- redact_pii(text) → removes PII from transcript
- extract_action_items(transcript) → extracts follow-up tasks
- diarize_audio(audio_path) → detects Speaker A / Speaker B
- process_transcript(segments) → master function

## Setup
1. Create virtual environment: python -m venv venv
2. Activate: venv\Scripts\Activate.ps1
3. Install: pip install -r requirements.txt
4. Create .env file with:
   - HF_TOKEN=your_huggingface_token
   - GROQ_API_KEY=your_groq_key

## Privacy Audit Result
✅ 10/10 PII test cases passed (100% accuracy)

## Tech Stack
- Pyannote.audio - Speaker Diarization
- Microsoft Presidio - PII Detection
- Groq Llama 3 - Action Items
- Spacy - NLP backbone