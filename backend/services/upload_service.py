import os
import shutil
from pathlib import Path
from datetime import datetime
from utils.logger import logger
from fastapi import UploadFile

from config import UPLOAD_FOLDER
from utils.file_utils import (
    validate_extension,
    validate_file_size,
    generate_filename,
)
from schemas.upload import UploadResponse


def save_uploaded_file(file: UploadFile) -> UploadResponse:
    # Validate file extension
    validate_extension(file.filename)

    # Validate file size
    file_size = validate_file_size(file)

    # Generate unique filename
    unique_filename = generate_filename(file.filename)

    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # File path
    filepath = Path(UPLOAD_FOLDER) / unique_filename

    # Save file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return UploadResponse(
        success=True,
        message="File uploaded successfully",
        filename=unique_filename,
        original_filename=file.filename,
        file_size=file_size,
        file_type=Path(file.filename).suffix.lower(),
        upload_time=datetime.now(),
    )