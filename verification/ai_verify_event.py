import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def ai_verify_event(title):

    prompt = f"""
Determine if the following title refers to a real UX/design event 
(conference, meetup, summit, or workshop).

Title: "{title}"

Respond ONLY with YES or NO.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You classify UX industry events."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        answer = response.choices[0].message.content.strip().upper()

        return answer == "YES"

    except Exception as e:
        print("AI verification failed:", e)
        return False