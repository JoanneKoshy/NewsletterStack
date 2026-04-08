import json
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key)

MODEL = "llama-3.3-70b-versatile"


def extract_from_reports(file_contents: list[dict]) -> dict:
    combined_text = ""
    for f in file_contents:
        combined_text += f"\n\n--- START OF: {f['filename']} ---\n"
        combined_text += f["text"]
        combined_text += f"\n--- END OF: {f['filename']} ---\n"

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.1,
        max_tokens=4096,
        messages=[
            {
                "role": "system",
                "content": """You are a data extraction assistant for an investor newsletter.
Extract key information from the uploaded reports and return ONLY valid JSON
with no markdown formatting, no backticks, no preamble.

Return this exact structure:
{
    "company_name": "the company name if found",
    "period": "the reporting period",
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
            },
            {"role": "user", "content": combined_text},
        ],
    )

    response_text = response.choices[0].message.content.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
    if response_text.endswith("```"):
        response_text = response_text.rsplit("```", 1)[0]

    return json.loads(response_text.strip())


def generate_newsletter(extracted_data: dict, media_links: list = None, tone: str = "formal") -> str:
    """
    Generates the newsletter as clean Markdown (not HTML).
    Includes media links and images if provided.
    """
    media_section = ""
    if media_links:
        media_section = "\n\nMedia content to include in the newsletter:\n"
        for m in media_links:
            if m.get("type") == "image":
                media_section += f"- Image: ![{m.get('caption', '')}]({m.get('url', '')})\n"
            else:
                media_section += f"- {m.get('type', 'link').title()}: {m.get('url', '')} ({m.get('title', 'Untitled')})\n"

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        max_tokens=8192,
        messages=[
            {
                "role": "system",
                "content": f"""You are a professional investor relations writer. Tone: {tone} and corporate.

Generate a polished investor newsletter in MARKDOWN format.

Rules:
- Use clean Markdown that works on Substack
- Structure: Title (H1), Executive Summary, Financial Highlights, Key Wins,
  Progress Updates, Team Updates, Challenges, Outlook/Next Steps
- Include sections ONLY if data exists for them
- For financial data, use Markdown tables
- If media links are provided (YouTube, social posts), embed them naturally
  in relevant sections. For YouTube links, put the bare URL on its own line
  so Substack auto-embeds it
- For images, use standard Markdown image syntax
- Keep it concise, professional, and investor-friendly
- Return ONLY the Markdown. No code fences around the whole thing. No explanation.""",
            },
            {
                "role": "user",
                "content": f"Generate the investor newsletter from this data:\n\n{json.dumps(extracted_data, indent=2)}{media_section}",
            },
        ],
    )

    md = response.choices[0].message.content.strip()
    if md.startswith("```"):
        md = md.split("\n", 1)[1]
    if md.endswith("```"):
        md = md.rsplit("```", 1)[0]

    return md.strip()