from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["Health"]
)

@router.get("/health")
def health():
    return {
        "status": "running",
        "service": "VoiceOps Sentinel API"
    }