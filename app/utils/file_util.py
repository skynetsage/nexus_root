import os
import random
import string
from datetime import datetime

from fastapi import UploadFile
from app.core.config import settings


def allowed_file(filename: str, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = settings.upload.upload_allowed_types
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


async def save_file(file: UploadFile, filename: str) -> str:
    if not allowed_file(filename):
        raise ValueError("File type not allowed")

    os.makedirs(settings.upload.upload_folder, exist_ok=True)
    file_path = os.path.join(settings.upload.upload_folder, filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return file_path


def generate_custom_resume_id(prefix: str, length: int = 4):
    safe_prefix = prefix[:6].strip().upper().replace(" ", "")

    date = datetime.today().strftime("%Y%m%d")
    random_part = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=length)
    )
    return f"{safe_prefix}-{date}-{random_part}"
