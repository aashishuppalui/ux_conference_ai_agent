import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def extract_event_details(url):

    try:
        response = requests.get(url, timeout=10)
    except Exception:
        return None

    if response.status_code != 200:
        return None

    content = response.text[:6000]  # limit to reduce tokens

    prompt = f"""
Extract event details from this web page content.

Return JSON with fields:
name
location
date
online
price

Content:
{content}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You extract event details from web pages."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        text = completion.choices[0].message.content

        return text

    except Exception as e:
        print("Extraction failed:", e)
        return None