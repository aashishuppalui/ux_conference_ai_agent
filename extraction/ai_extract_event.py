import json
import os
import requests
from openai import OpenAI


def extract_event(url, title):

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = requests.get(url, timeout=10)
    except Exception:
        return None

    if response.status_code != 200:
        return None

    content = response.text[:5000]

    prompt = f"""
    You are analyzing a web page.

    Determine if this is a real UX/design event.

    If YES → return JSON ONLY:
    {{
    "name": "...",
    "location": "...",
    "date": "...",
    "online": "...",
    "price": "...",
    "official_url": "..."
    }}

IMPORTANT:
- official_url MUST be the actual event page (Eventbrite, Meetup, or official website)
- NOT a news article or blog

If NOT → return: NULL

Title: {title}

Content:
{content}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You extract structured event data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        result = completion.choices[0].message.content.strip()

        # If AI says not an event
        if "NULL" in result.upper():
            return None
        
        # Clean AI output
        cleaned = result

        # Remove markdown
        cleaned = cleaned.replace("```json", "").replace("```", "")

        # Remove junk characters
        cleaned = cleaned.replace("**", "").strip()

        # Ensure JSON starts with { and ends with }
        if not cleaned.startswith("{"):
            cleaned = "{" + cleaned
        if not cleaned.endswith("}"):
            cleaned = cleaned + "}"


        # Try parsing JSON
        try:
            return json.loads(cleaned)
        except Exception:
            print("JSON parse failed:", cleaned)
            return None

    except Exception as e:
        print("Extraction failed:", e)
        return None