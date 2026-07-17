import os
import uuid
from pathlib import Path

from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


def validate_extension(filename: str):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )


def validate_file_size(file):
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise ValueError("File size exceeds 25 MB")

    return size


def generate_filename(filename: str):
    extension = Path(filename).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{extension}"
    return unique_name