from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from services.transcriber import transcribe_audio

router = APIRouter(
    prefix="/transcribe",
    tags=["Transcription"]
)

UPLOAD_DIR = "uploads"


@router.post("/")
async def transcribe(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        result = transcribe_audio(file_path)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )