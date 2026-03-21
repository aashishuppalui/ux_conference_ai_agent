import os
import json
import sys
import argparse
import requests
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
# from discovery.eventbrite import discover_eventbrite_events
from utils.event_filter import is_valid_event
from discovery.rss_search import discover_rss_events
from verification.ai_verify_event import ai_verify_event
from extraction.extract_event_details import extract_event_details


CURRENT_YEARS = ["2026", "2025"]


# -------- LOAD SEED LIST -------- #

def load_seed_conferences():
    with open("data/seed_conferences.json", "r") as f:
        return json.load(f)


# -------- CHECK WEBSITE FOR CURRENT YEAR -------- #

def detect_current_edition(conference):
    try:
        response = requests.get(
            conference["website"],
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
    except Exception:
        return None

    if response.status_code != 200:
        return None

    page_text = response.text.lower()

    for year in CURRENT_YEARS:
        if year in page_text:
            return year

    return None


# -------- FETCH CONFIRMED EVENTS -------- #

def get_events():
    seed_list = load_seed_conferences()
    all_events = []

# -------- Seed Conferences -------- #
    for conf in seed_list:
        detected_year = detect_current_edition(conf)

        if not detected_year:
            continue

        all_events.append({
            "name": f"{conf['name']} {detected_year}",
            "location": conf.get("country", "Unknown"),
            "date": detected_year,
            "online": "Unknown",
            "price": "Unknown",
            "free": "Unknown",
            "url": conf["website"],
        })

     # -------- RSS Discovery -------- #
    seen_titles = set()

    try:
        rss_events = discover_rss_events()

        print(f"RSS discovered: {len(rss_events)} events")
        for e in rss_events[:10]:
            print("DISCOVERED:", e["name"])

        for event in rss_events:
            title_key = event["name"].lower()

            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)
            
            if not ai_verify_event(event["name"]):
                continue

            all_events.append(event)

    except Exception as e:
        print("RSS discovery failed:", e)

    return all_events


# -------- MAIN -------- #

def main(dry_run: bool = False) -> int:
    events = get_events()

    if dry_run:
        print("Detected conferences:")
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