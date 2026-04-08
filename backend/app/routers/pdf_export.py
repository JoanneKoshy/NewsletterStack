from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.pdf_service import generate_pdf

router = APIRouter()


class PDFRequest(BaseModel):
    html_content: str
    filename: str = "Investor_Newsletter"


@router.post("/export-pdf")
async def export_pdf(req: PDFRequest):
    try:
        output_file = generate_pdf(req.html_content, req.filename)
        return FileResponse(
            output_file,
            media_type="application/pdf",
            filename=f"{req.filename}.pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")