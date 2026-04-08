from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.file_parser import parse_file
from app.services.claude_service import extract_from_reports

router = APIRouter()


class ExtractionRequest(BaseModel):
    files: list[dict]


@router.post("/extract")
async def extract_data(req: ExtractionRequest):
    try:
        file_contents = []

        for f in req.files:
            text = parse_file(f["path"])
            file_contents.append({
                "filename": f["original_name"],
                "text": text,
            })

        result = extract_from_reports(file_contents)

        return {"extracted_data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))