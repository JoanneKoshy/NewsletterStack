import json
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key)

MODEL = "llama-3.1-8b-instant"


def extract_from_reports(file_contents: list[dict]) -> dict:
    combined_text = ""
    for f in file_contents:
        combined_text += f"\n--- {f['filename']} ---\n"
        combined_text += f["text"]

    words = combined_text.split()
    if len(words) > 2000:
        combined_text = " ".join(words[:2000])

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.1,
        max_tokens=1500,
        messages=[
            {
                "role": "system",
                "content": """Extract business info from reports. Return ONLY valid JSON:
{"company_name":"...","period":"...","financial_highlights":{"revenue":"...","expenses":"...","net_profit":"...","payables":"...","receivables":"...","other_metrics":[{"label":"...","value":"..."}]},"key_wins":["..."],"progress_updates":["..."],"new_hires":["..."],"challenges":["..."],"upcoming":["..."],"raw_summary":"..."}
Use null or [] if no data. No markdown. No backticks.""",
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
    compact_data = json.dumps(extracted_data, separators=(",", ":"))

    if len(compact_data) > 6000:
        compact_data = compact_data[:6000]

    # Build explicit media instructions
    media_instruction = ""
    if media_links and len(media_links) > 0:
        media_instruction = "\n\nIMPORTANT — Include these media items in the newsletter. Copy them EXACTLY as written:\n"
        for i, m in enumerate(media_links):
            if m.get("type") == "image":
                media_instruction += f"\nImage {i+1} — put this in the newsletter:\n![{m.get('title','')}]({m.get('url','')})\n"
            elif m.get("type") == "youtube":
                media_instruction += f"\nYouTube video {i+1} — put this URL on its own line in the newsletter:\n{m.get('url','')}\n"
            else:
                media_instruction += f"\nLink {i+1} — embed in newsletter:\n[{m.get('title','Link')}]({m.get('url','')})\n"

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": f"""Write a {tone} investor newsletter in Markdown.
Use # title, ## sections, tables for financials.
Only include sections with data.
Return ONLY Markdown. No code fences.""",
            },
            {"role": "user", "content": f"{compact_data}{media_instruction}"},
        ],
    )

    md = response.choices[0].message.content.strip()
    if md.startswith("```"):
        md = md.split("\n", 1)[1]
    if md.endswith("```"):
        md = md.rsplit("```", 1)[0]

    # If the model forgot to include media, append them at the end
    if media_links:
        for m in media_links:
            url = m.get("url", "")
            if url and url not in md:
                if m.get("type") == "image":
                    md += f"\n\n![{m.get('title', '')}]({url})"
                elif m.get("type") == "youtube":
                    md += f"\n\n{url}"
                else:
                    md += f"\n\n[{m.get('title', 'Link')}]({url})"

    return md.strip()