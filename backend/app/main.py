from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, extract, newsletter, email_sender, pdf_export, investors

app = FastAPI(title="Investor Newsletter Tool")

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route files
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(extract.router, prefix="/api", tags=["extract"])
app.include_router(newsletter.router, prefix="/api", tags=["newsletter"])
app.include_router(email_sender.router, prefix="/api", tags=["email"])
app.include_router(pdf_export.router, prefix="/api", tags=["pdf"])
app.include_router(investors.router, prefix="/api", tags=["investors"])


@app.get("/api/health")
async def health():
    return {"status": "ok"}