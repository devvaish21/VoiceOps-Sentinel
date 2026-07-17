from pydantic import BaseModel
from datetime import datetime


class UploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    upload_time: datetime