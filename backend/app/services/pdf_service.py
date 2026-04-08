import os
import uuid
from xhtml2pdf import pisa
from app.config import settings


def generate_pdf(html_content: str, filename: str = "Investor_Newsletter") -> str:
    os.makedirs(settings.output_dir, exist_ok=True)

    output_file = os.path.join(
        settings.output_dir, f"{filename}_{uuid.uuid4().hex[:8]}.pdf"
    )

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 1.5cm; }}
        body {{ font-family: Arial, Helvetica, sans-serif; font-size: 12px; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

    with open(output_file, "wb") as f:
        pisa.CreatePDF(full_html, dest=f)

    return output_file


