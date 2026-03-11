import requests
import xml.etree.ElementTree as ET


SEARCH_QUERY = "ux conference OR ux summit OR ux meetup"


def discover_rss_events():

    url = f"https://news.google.com/rss/search?q={SEARCH_QUERY}"

    events = []

    try:
        response = requests.get(url, timeout=10)
    except Exception:
        print("RSS fetch failed")
        return events

    root = ET.fromstring(response.content)

    for item in root.findall(".//item"):

        title = item.find("title").text
        link = item.find("link").text

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