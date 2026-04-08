from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.file_parser import parse_file
from app.services.claude_service import extract_from_reports, extract_from_pdf_native
import json

router = APIRouter()


class ExtractionRequest(BaseModel):
    files: list[dict]
    use_native_pdf: bool = True


@router.post("/extract")
async def extract_data(req: ExtractionRequest):
    try:
        file_contents = []

        for f in req.files:
            if req.use_native_pdf and f["type"] == ".pdf":
                # Send PDF directly to Claude (better for tables/charts)
                extraction = extract_from_pdf_native(f["path"], f["original_name"])
                # Wrap it as text so we can merge with other files
                file_contents.append({
                    "filename": f["original_name"],
                    "text": json.dumps(extraction, indent=2),
                })
            else:
                # Extract text locally, then send to Claude
                text = parse_file(f["path"])
                file_contents.append({
                    "filename": f["original_name"],
                    "text": text,
                })

        # Send everything to Claude for unified extraction
        result = extract_from_reports(file_contents)

        return {"extracted_data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))