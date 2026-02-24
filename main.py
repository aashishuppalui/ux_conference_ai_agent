import os
import json
import sys
import argparse
import gspread
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from google.oauth2.service_account import Credentials


# -------- SEARCH QUERIES --------
SEARCH_QUERIES = [
    "AI conference 2026",
    "Tech summit 2026",
    "UX conference 2026",
    "Developer conference 2026",
    "Product design summit 2026"
]

TECH_KEYWORDS = [
    "ux", "ui", "design", "ai", "developer",
    "tech", "product", "software", "engineering"
]

CONF_KEYWORDS = [
    "conference", "summit", "meetup",
    "expo", "forum", "symposium", "workshop"
]


# -------- FETCH FROM GOOGLE NEWS RSS --------
def fetch_from_eventbrite():
    url = "https://www.eventbrite.com/d/online/ux-conference/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print("Eventbrite fetch failed")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    cards = soup.select("div.eds-event-card-content__content")[:20]

    for card in cards:
        title_tag = card.select_one("div.eds-event-card-content__primary-content")
        link_tag = card.find_parent("a")

        if not title_tag or not link_tag:
            continue

        title = title_tag.text.strip()
        link = link_tag["href"]

        title_lower = title.lower()

        if "ux" not in title_lower and "user experience" not in title_lower:
            continue

        events.append({
            "name": title,
            "location": "Unknown",
            "date": "Unknown",
            "online": "Unknown",
            "price": "Unknown",
            "free": "Unknown",
            "url": link,
        })

    return events


def get_events():
    events = []

    eb_events = fetch_from_eventbrite()
    events.extend(eb_events)

    return events


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