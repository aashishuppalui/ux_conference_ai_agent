import os
import json
import sys
import argparse
import gspread
import feedparser
from datetime import datetime
from google.oauth2.service_account import Credentials


# -------- GLOBAL KEYWORDS (Scope C: Tech + Design) --------
KEYWORDS = [
    "ux", "ui", "design", "frontend", "ai",
    "machine learning", "product", "tech",
    "developer", "innovation", "startup"
]


# -------- FETCH EVENTS FROM RSS --------
def fetch_from_rss():
    rss_url = "https://dev.to/feed/tag/events"
    feed = feedparser.parse(rss_url)

    events = []

    for entry in feed.entries[:20]:
        title_lower = entry.title.lower()

        # Keyword filtering
        if not any(keyword in title_lower for keyword in KEYWORDS):
            continue

        events.append({
            "name": entry.title,
            "location": "Online",
            "date": "Unknown",
            "online": "Yes",
            "price": "Unknown",
            "free": "Unknown",
            "url": entry.link,
        })

    return events


# -------- MASTER EVENT COLLECTOR --------
def get_events():
    events = []

    rss_events = fetch_from_rss()
    events.extend(rss_events)

    return events


def main(dry_run: bool = False) -> int:
    events = get_events()

    if dry_run:
        print("Dry run: would append the following rows to the sheet:")
        for event in events:
            row = [
                event["name"],
                event["location"],
                event["date"],
                event["online"],
                event["price"],
                event["free"],
                event["url"],
                datetime.today().strftime("%Y-%m-%d"),
            ]
            print(row)
        return 0

    # -------- AUTH USING GITHUB SECRET --------
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

    # -------- DUPLICATE CHECK --------
    existing_records = sheet.get_all_records()
    existing_urls = {row["URL"] for row in existing_records if "URL" in row}

    new_events_added = 0

    for event in events:
        if event["url"] in existing_urls:
            print(f"Skipping duplicate event: {event['name']}")
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