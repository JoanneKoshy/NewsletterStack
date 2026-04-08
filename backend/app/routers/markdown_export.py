import os
import uuid
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.config import settings

router = APIRouter()


class MarkdownExportRequest(BaseModel):
    markdown: str
    filename: str = "Investor_Newsletter"


@router.post("/export-markdown")
async def export_markdown(req: MarkdownExportRequest):
    """Download the newsletter as a .md file."""
    os.makedirs(settings.output_dir, exist_ok=True)

    output_file = os.path.join(
        settings.output_dir, f"{req.filename}_{uuid.uuid4().hex[:8]}.md"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(req.markdown)

    return FileResponse(
        output_file,
        media_type="text/markdown",
        filename=f"{req.filename}.md",
    )