from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.claude_service import generate_newsletter

router = APIRouter()


class GenerateRequest(BaseModel):
    extracted_data: dict
    tone: str = "formal"


class RegenerateRequest(BaseModel):
    extracted_data: dict
    feedback: str
    tone: str = "formal"


@router.post("/generate-newsletter")
async def create_newsletter(req: GenerateRequest):
    try:
        html = generate_newsletter(req.extracted_data, req.tone)
        return {"html": html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/regenerate-newsletter")
async def regenerate_newsletter(req: RegenerateRequest):
    try:
        # Add Robin's feedback so Claude knows what to change
        req.extracted_data["_user_feedback"] = req.feedback
        html = generate_newsletter(req.extracted_data, req.tone)
        return {"html": html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))