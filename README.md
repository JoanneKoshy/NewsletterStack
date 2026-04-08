---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/upload` | Upload PDF/DOCX report files |
| POST | `/api/extract` | Extract structured data from reports using AI |
| POST | `/api/media/link` | Add a YouTube/social media link |
| POST | `/api/media/image` | Upload an image or infographic |
| POST | `/api/generate-newsletter` | Generate Markdown newsletter from extracted data |
| POST | `/api/regenerate-newsletter` | Regenerate with user feedback |
| POST | `/api/save-edit` | Save edited markdown |
| POST | `/api/export-markdown` | Download newsletter as .md file |
| POST | `/api/export-pdf` | Download newsletter as PDF |

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- Groq API key (free at https://console.groq.com/keys)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

Create `backend/.env`:
