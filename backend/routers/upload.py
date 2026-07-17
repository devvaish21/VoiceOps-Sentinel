from fastapi import APIRouter, File, HTTPException, UploadFile

from schemas.upload import UploadResponse
from services.upload_service import save_uploaded_file

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("/", response_model=UploadResponse)
async def upload_audio(file: UploadFile = File(...)):
    try:
        return save_uploaded_file(file)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}",
        )