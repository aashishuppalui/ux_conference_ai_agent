import os
import json
import sys
import argparse
import gspread
import feedparser
from datetime import datetime
from google.oauth2.service_account import Credentials


# ---------------- SEARCH CONFIG ---------------- #

SEARCH_QUERIES = [
    '"UX Conference 2026"',
    '"User Experience Conference 2026"',
    '"Interaction Design Conference 2026"',
    '"Design Systems Conference 2026"',
    '"UX Summit 2026"',
    '"UX Conference 2025"',
]

ALLOWED_DOMAINS = [
    "eventbrite.com",
    "meetup.com",
    "interaction-design.org",
    "smashingmagazine.com",
    "nngroup.com",
    "ixda.org",
]

TECH_KEYWORDS = [
    "ux",
    "user experience",
    "interaction design",
    "design systems",
]

CONF_KEYWORDS = [
    "conference",
    "summit",
    "symposium",
    "forum",
    "workshop",
]


# ---------------- GOOGLE RSS FETCH ---------------- #

def fetch_from_google_news():
    events = []

    for query in SEARCH_QUERIES:
        rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}"
        feed = feedparser.parse(rss_url)

        for entry in feed.entries[:20]:
            title = entry.title
            title_lower = title.lower()

            score = 0

            # Positive signals
            if "conference" in title_lower:
                score += 2
            if "summit" in title_lower:
                score += 2
            if "2026" in title_lower or "2025" in title_lower:
                score += 2
            if "ux" in title_lower or "user experience" in title_lower:
                score += 2

            # Negative signals
            if "blog" in title_lower:
                score -= 2
            if "news" in title_lower:
                score -= 1

            if score < 4:
                continue

            events.append({
                "name": title,
                "location": "Unknown",
                "date": "Unknown",
                "online": "Unknown",
                "price": "Unknown",
                "free": "Unknown",
                "url": entry.link,
            })

    return events

# ---------------- MASTER EVENT COLLECTOR ---------------- #

def get_events():
    return fetch_from_google_news()


# ---------------- MAIN ---------------- #

def main(dry_run: bool = False) -> int:
    events = get_events()

    if dry_run:
        print("Dry run preview:")
        for e in events:
            print(e)
        return 0

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds_json = os.environ.get("GOOGLE_CREDENTIALS")

    if not creds_json:
        print("GOOGLE_CREDENTIALS environment variable not found.", file=sys.stderr)
        return 2

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

    client = gspread.authorize(creds)
    sheet = client.open("UX_UI_Conferences").sheet1

    existing_records = sheet.get_all_records()
    existing_urls = {row["URL"] for row in existing_records if "URL" in row}

    new_events_added = 0

    for event in events:
        if event["url"] in existing_urls:
            continue

        sheet.append_row([
            event["name"],
            event["location"],
            event["date"],
            event["online"],
            event["price"],
            event["free"],
            event["url"],
            datetime.today().strftime("%Y-%m-%d"),
        ])

        new_events_added += 1
        print(f"Added: {event['name']}")

    print(f"Total new events added: {new_events_added}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    sys.exit(main(dry_run=args.dry_run))