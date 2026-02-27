import os
import json
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

# -------- LLM SWITCH --------
LLM_PROVIDER = "gemini"  # change to "openai" anytime

LOOKBACK_DAYS = 14


def get_recent_events(sheet):
    rows = sheet.get_all_records()
    cutoff = datetime.today() - timedelta(days=LOOKBACK_DAYS)

    recent = []
    for r in rows:
        added = datetime.strptime(r["Added On"], "%Y-%m-%d")
        if added >= cutoff:
            recent.append(r)

    return recent


# ---------- GEMINI ----------
def generate_with_gemini(prompt):
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    response = model.generate_content(prompt)

    return response.text


# ---------- OPENAI ----------
def generate_with_openai(prompt):
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def generate_post(events):

    events_text = "\n".join(
        [f"- {e['Name']} ({e['Location']})" for e in events]
    )

    prompt = f"""
Write a professional LinkedIn post for UX designers.

Tone:
- insightful
- concise
- human
- not promotional

These UX conferences were recently detected:

{events_text}

Include:
• short intro
• bullet list
• closing insight
• 3 relevant hashtags
"""

    if LLM_PROVIDER == "gemini":
        return generate_with_gemini(prompt)

    if LLM_PROVIDER == "openai":
        return generate_with_openai(prompt)


def main():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_info(
        json.loads(os.environ["GOOGLE_CREDENTIALS"]),
        scopes=scope,
    )

    gc = gspread.authorize(creds)
    sheet = gc.open("UX_UI_Conferences").sheet1

    events = get_recent_events(sheet)

    if not events:
        print("No recent events.")
        return

    post = generate_post(events)

    with open("linkedin_post.txt", "w", encoding="utf-8") as f:
        f.write(post)

    print("LinkedIn post generated using", LLM_PROVIDER)


if __name__ == "__main__":
    main()