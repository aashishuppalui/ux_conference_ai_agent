import os
import json
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
from openai import OpenAI


# ---------- CONFIG ----------
DAYS_LOOKBACK = 14


def get_recent_events(sheet):
    records = sheet.get_all_records()

    cutoff = datetime.today() - timedelta(days=DAYS_LOOKBACK)

    recent = []

    for r in records:
        added = datetime.strptime(r["Added On"], "%Y-%m-%d")

        if added >= cutoff:
            recent.append(r)

    return recent


def generate_linkedin_post(events):

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    events_text = "\n".join(
        [f"- {e['Name']} ({e['Location']})" for e in events]
    )

    prompt = f"""
Write a professional LinkedIn post for UX designers.

Tone:
- insightful
- concise
- friendly
- not salesy

Content:
These UX conferences were recently announced:

{events_text}

Add:
- short intro
- bullet list
- closing reflection
- 3 relevant hashtags
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def main():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_info(
        json.loads(os.environ["GOOGLE_CREDENTIALS"]),
        scopes=scope,
    )

    client = gspread.authorize(creds)
    sheet = client.open("UX_UI_Conferences").sheet1

    events = get_recent_events(sheet)

    if not events:
        print("No new events found.")
        return

    post = generate_linkedin_post(events)

    with open("linkedin_post.txt", "w", encoding="utf-8") as f:
        f.write(post)

    print("LinkedIn post generated!")


if __name__ == "__main__":
    main()