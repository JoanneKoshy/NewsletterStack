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
    type: str = "youtube"  # youtube, twitter, instagram, linkedin, other


@router.post("/media/link")
async def add_media_link(link: MediaLink):
    """Store a social media link to include in the newsletter."""
    return {
        "url": link.url,
        "title": link.title,
        "type": link.type,
        "embed_markdown": generate_embed_markdown(link.url, link.title, link.type),
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

    return {
        "filename": file.filename,
        "stored_name": unique_name,
        "url": f"http://localhost:8000/uploads/{unique_name}",
        "caption": caption,
        "markdown": f"![{caption or file.filename}](http://localhost:8000/uploads/{unique_name})",
    }

def generate_embed_markdown(url: str, title: str, link_type: str) -> str:
    """Generate Substack-friendly markdown for a media link."""
    if link_type == "youtube":
        # Extract video ID
        video_id = ""
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        elif "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]

        if video_id:
            # Substack auto-embeds YouTube links on their own line
            return f"\n{url}\n"

    # For all other links, just format as a titled link
    display_title = title or url
    return f"[{display_title}]({url})"