import json
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key)

# gemma2-9b-it has 15,000 TPM on free tier — best balance
EXTRACT_MODEL = "gemma2-9b-it"
GENERATE_MODEL = "gemma2-9b-it"


def extract_from_reports(file_contents: list[dict]) -> dict:
    combined_text = ""
    for f in file_contents:
        combined_text += f"\n\n--- START OF: {f['filename']} ---\n"
        combined_text += f["text"]
        combined_text += f"\n--- END OF: {f['filename']} ---\n"

    # Truncate to stay under token limits
    words = combined_text.split()
    if len(words) > 4000:
        combined_text = " ".join(words[:4000])
        combined_text += "\n\n[Document truncated due to length]"

    response = client.chat.completions.create(
        model=EXTRACT_MODEL,
        temperature=0.1,
        max_tokens=2048,
        messages=[
            {
                "role": "system",
                "content": """Extract key business info from the reports. Return ONLY valid JSON, no markdown, no backticks.

{
    "company_name": "name or null",
    "period": "reporting period or null",
    "financial_highlights": {
        "revenue": "amount or null",
        "expenses": "amount or null",
        "net_profit": "amount or null",
        "payables": "amount or null",
        "receivables": "amount or null",
        "other_metrics": [{"label": "...", "value": "..."}]
    },
    "key_wins": ["achievements"],
    "progress_updates": ["progress items"],
    "new_hires": ["new team members"],
    "challenges": ["challenges"],
    "upcoming": ["next steps"],
    "raw_summary": "2-3 sentence summary"
}""",
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
    # Keep the data compact to stay under token limits
    compact_data = json.dumps(extracted_data, separators=(",", ":"))

    media_section = ""
    if media_links:
        media_section = "\n\nMedia to embed:\n"
        for m in media_links:
            if m.get("type") == "image":
                media_section += f"- Image: ![{m.get('title', '')}]({m.get('url', '')})\n"
            else:
                media_section += f"- {m.get('type', 'link')}: {m.get('url', '')} - {m.get('title', '')}\n"

    response = client.chat.completions.create(
        model=GENERATE_MODEL,
        temperature=0.3,
        max_tokens=3000,
        messages=[
            {
                "role": "system",
                "content": f"""You are an investor relations writer. Tone: {tone}, corporate.
Write a Markdown newsletter. Rules:
- Use # for title, ## for sections, tables for financials
- Only include sections with data
- For YouTube links, put bare URL on its own line
- For images, use ![caption](url)
- Sections: Title, Executive Summary, Financial Highlights, Key Wins, Progress, Team, Challenges, Outlook
- Return ONLY Markdown, no code fences, no explanation""",
            },
            {
                "role": "user",
                "content": f"Data:\n{compact_data}{media_section}",
            },
        ],
    )

    md = response.choices[0].message.content.strip()
    if md.startswith("```"):
        md = md.split("\n", 1)[1]
    if md.endswith("```"):
        md = md.rsplit("```", 1)[0]

    return md.strip()