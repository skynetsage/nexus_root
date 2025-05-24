from pathlib import Path
import aiofiles
from fastapi import UploadFile
from ..config.upload import upload_config
from .config_util import PROJECT_ROOT

def allowed_file_type(filename: str, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = upload_config.allowed_file_types
    return filename.split(".")[-1].lower() in allowed_extensions

async def upload_file(file: UploadFile) -> str:
    if not allowed_file_type(file.filename):
        raise ValueError(f"File type not allowed: {file.filename}")

    relative_path = upload_config.upload_folder / file.filename
    absolute_path = PROJECT_ROOT / relative_path

    absolute_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(absolute_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return str(relative_path)
