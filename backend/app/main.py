from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, extract, newsletter, media, markdown_export, pdf_export, hashnode
from app.config import settings
import os

app = FastAPI(title="Investor Newsletter Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images so frontend can display them
os.makedirs(settings.upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(media.router, prefix="/api", tags=["media"])
app.include_router(extract.router, prefix="/api", tags=["extract"])
app.include_router(newsletter.router, prefix="/api", tags=["newsletter"])
app.include_router(markdown_export.router, prefix="/api", tags=["markdown"])
app.include_router(pdf_export.router, prefix="/api", tags=["pdf"])
app.include_router(hashnode.router, prefix="/api", tags=["hashnode"])


@app.get("/api/health")
async def health():
    return {"status": "ok"}