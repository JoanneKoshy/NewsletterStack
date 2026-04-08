from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.claude_service import generate_newsletter

router = APIRouter()


class GenerateRequest(BaseModel):
    extracted_data: dict
    media_links: list = []
    tone: str = "formal"


class RegenerateRequest(BaseModel):
    extracted_data: dict
    media_links: list = []
    feedback: str
    tone: str = "formal"


class EditRequest(BaseModel):
    markdown: str


@router.post("/generate-newsletter")
async def create_newsletter(req: GenerateRequest):
    try:
        markdown = generate_newsletter(req.extracted_data, req.media_links, req.tone)
        return {"markdown": markdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/regenerate-newsletter")
async def regenerate_newsletter(req: RegenerateRequest):
    try:
        req.extracted_data["_user_feedback"] = req.feedback
        markdown = generate_newsletter(req.extracted_data, req.media_links, req.tone)
        return {"markdown": markdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save-edit")
async def save_edit(req: EditRequest):
    """Robin edits the markdown directly — this just acknowledges the save."""
    return {"markdown": req.markdown, "status": "saved"}