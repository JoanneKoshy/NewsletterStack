import os
import uuid
from fastapi import APIRouter, UploadFile, File
from app.config import settings

router = APIRouter()


@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    saved_files = []
    os.makedirs(settings.upload_dir, exist_ok=True)

    for file in files:
        # Only allow PDF, DOCX, TXT
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in (".pdf", ".docx", ".doc", ".txt"):
            continue

        # Save with unique name to avoid overwriting
        unique_name = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(settings.upload_dir, unique_name)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        saved_files.append({
            "original_name": file.filename,
            "stored_name": unique_name,
            "path": file_path,
            "size": len(content),
            "type": ext,
        })

    return {"files": saved_files, "count": len(saved_files)}