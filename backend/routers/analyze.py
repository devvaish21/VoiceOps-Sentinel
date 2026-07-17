from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from services.transcriber import transcribe_audio
from services.summarizer import generate_summary
from services.sentiment import analyze_sentiment
from services.pii_detector import detect_pii
from services.action_items import extract_action_items

router = APIRouter(
    prefix="/analyze",
    tags=["AI Analysis"]
)

UPLOAD_DIR = "uploads"


@router.post("/")
async def analyze(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        transcript = transcribe_audio(file_path)

        text = transcript["transcript"]

        return {
            "transcript": text,
            "language": transcript["language"],
            "summary": generate_summary(text),
            "sentiment": analyze_sentiment(text),
            "pii": detect_pii(text),
            "action_items": extract_action_items(text)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )