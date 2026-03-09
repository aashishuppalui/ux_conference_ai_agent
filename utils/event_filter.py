CONFERENCE_KEYWORDS = [
    "conference",
    "summit",
    "meetup",
    "workshop",
    "ux",
    "design",
]

EXCLUDED_KEYWORDS = [
    "course",
    "bootcamp",
    "diploma",
    "training",
    "certification",
    "degree",
]


def is_valid_event(title):

    title_lower = title.lower()

    if any(bad in title_lower for bad in EXCLUDED_KEYWORDS):
        return False

    if any(good in title_lower for good in CONFERENCE_KEYWORDS):
        return True

    return False