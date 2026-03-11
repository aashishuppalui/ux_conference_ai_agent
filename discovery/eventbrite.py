from wsgiref import headers

import requests
from bs4 import BeautifulSoup


SEARCH_URL = "https://www.eventbrite.com/d/online/ux/"


def discover_eventbrite_events():
    events = []

    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(
    SEARCH_URL,
    headers=headers,
    timeout=15
    )

    response = requests.get(SEARCH_URL, headers=headers, timeout=10)

    if response.status_code != 200:
        print("Failed to fetch Eventbrite page", response.status_code)
        return events

    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.find_all("a", href=True)

    for card in cards:

        title = card.get_text(strip=True)
        link = card["href"]

        if not title:
            continue

        title_lower = title.lower()

        keywords = [
            "ux",
            "user experience",
            "design conference",
            "design summit",
            "ux meetup"
        ]

        if any(k in title_lower for k in keywords):

            events.append({
                "name": title,
                "location": "Unknown",
                "date": "Unknown",
                "online": "Unknown",
                "price": "Unknown",
                "free": "Unknown",
                "url": link
            })

    return events