import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.config import settings

router = APIRouter()


class MediaLink(BaseModel):
    url: str
    title: str = ""
    type: str = "youtube"


@router.post("/media/link")
async def add_media_link(link: MediaLink):
    return {
        "url": link.url,
        "title": link.title,
        "type": link.type,
    }


@router.post("/media/image")
async def upload_image(file: UploadFile = File(...), caption: str = Form("")):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
        return JSONResponse(status_code=400, content={"error": "Only image files allowed"})

    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(settings.upload_dir, unique_name)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    full_url = f"http://localhost:8000/uploads/{unique_name}"

    return {
        "filename": file.filename,
        "stored_name": unique_name,
        "url": full_url,
        "caption": caption,
    }