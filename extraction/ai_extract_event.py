import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def extract_event(url, title):

    try:
        response = requests.get(url, timeout=10)
    except Exception:
        return None

    if response.status_code != 200:
        return None

    content = response.text[:5000]

    prompt = f"""
You are analyzing a web page.

Determine if this is a real UX/design event (conference, meetup, workshop, summit).

If YES → extract details in JSON:
name, location, date, online, price

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

        if "NULL" in result.upper():
            return None

        return result

    except Exception as e:
        print("Extraction failed:", e)
        return None