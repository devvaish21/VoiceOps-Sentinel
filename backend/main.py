from fastapi import FastAPI

from routers.health import router as health_router
from routers.upload import router as upload_router
from routers.transcribe import router as transcribe_router

app = FastAPI(
    title="VoiceOps Sentinel API",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(transcribe_router)

@app.get("/")
def home():
    return {
        "application": "VoiceOps Sentinel",
        "version": "1.0.0",
        "status": "Running"
    }