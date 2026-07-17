from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "uploads"

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a"}

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB