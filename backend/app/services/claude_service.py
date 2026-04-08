import json
import base64
import anthropic
from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

MODEL = "claude-sonnet-4-6"


def extract_from_reports(file_contents: list[dict]) -> dict:
    """
    Takes a list of {"filename": "...", "text": "..."} dicts.
    Returns structured data extracted by Claude.
    """
    combined_text = ""
    for f in file_contents:
        combined_text += f"\n\n--- START OF: {f['filename']} ---\n"
        combined_text += f["text"]
        combined_text += f"\n--- END OF: {f['filename']} ---\n"

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system="""You are a data extraction assistant for an investor newsletter.
Extract key information from the uploaded reports and return ONLY valid JSON
with no markdown formatting, no backticks, no preamble.

Return this exact structure:
{
    "company_name": "the company name if found",
    "period": "the reporting period (e.g. 'Week ending March 28, 2026')",
    "financial_highlights": {
        "revenue": "amount or null",
        "expenses": "amount or null",
        "net_profit": "amount or null",
        "payables": "amount or null",
        "receivables": "amount or null",
        "other_metrics": [{"label": "...", "value": "..."}]
    },
    "key_wins": ["list of achievements, milestones, deals closed"],
    "progress_updates": ["list of project/product progress items"],
    "new_hires": ["list of new team members with roles if mentioned"],
    "challenges": ["list of challenges or risks mentioned"],
    "upcoming": ["list of upcoming plans, goals, next steps"],
    "raw_summary": "A 2-3 sentence executive summary of all reports combined"
}

If a field has no data, use null or an empty list. Do not fabricate data.""",
        messages=[
            {"role": "user", "content": combined_text}
        ],
    )

    response_text = message.content[0].text.strip()

    # Clean up if Claude wraps response in code fences
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
    if response_text.endswith("```"):
        response_text = response_text.rsplit("```", 1)[0]

    return json.loads(response_text.strip())


def extract_from_pdf_native(file_path: str, filename: str) -> dict:
    """
    Uses Claude's native PDF support — sends the actual PDF
    as base64 instead of extracted text. Much better for
    reading tables, charts, and complex layouts.
    """
    with open(file_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system="""You are a data extraction assistant. Extract all key business
information from this document. Return ONLY valid JSON with no markdown.

Return this structure:
{
    "filename": "the filename",
    "financials": {
        "revenue": "amount or null",
        "expenses": "amount or null",
        "payables": "amount or null",
        "receivables": "amount or null"
    },
    "key_points": ["list of important points"],
    "metrics": [{"label": "...", "value": "..."}],
    "summary": "2-3 sentence summary"
}""",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": f"Extract all key business data from this report: {filename}",
                    },
                ],
            }
        ],
    )

    response_text = message.content[0].text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
    if response_text.endswith("```"):
        response_text = response_text.rsplit("```", 1)[0]

    return json.loads(response_text.strip())


def generate_newsletter(extracted_data: dict, tone: str = "formal") -> str:
    """
    Takes the extracted data and generates a polished HTML newsletter.
    Returns raw HTML string.
    """
    message = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        system=f"""You are a professional investor relations writer. Your tone is
{tone} and corporate. Generate a polished investor newsletter in HTML format.

Rules:
- Use clean, inline-styled HTML suitable for email clients
- Professional color scheme: dark navy (#1a1a2e) headers, white body, subtle borders
- Include sections ONLY if data exists for them
- Use tables for financial data with proper formatting
- Keep it concise but comprehensive
- No images or external resources — everything inline
- All CSS must be inline styles (no <style> blocks), because email clients strip them
- Structure: Company header with period, Executive Summary, Financial Highlights,
  Key Wins & Milestones, Progress Updates, Team Updates, Challenges, Outlook
- Return ONLY the HTML. No markdown fences. No explanation.""",
        messages=[
            {
                "role": "user",
                "content": f"Generate the investor newsletter from this extracted data:\n\n{json.dumps(extracted_data, indent=2)}",
            }
        ],
    )

    html = message.content[0].text.strip()
    if html.startswith("```"):
        html = html.split("\n", 1)[1]
    if html.endswith("```"):
        html = html.rsplit("```", 1)[0]

    return html.strip()