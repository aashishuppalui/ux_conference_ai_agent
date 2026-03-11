EVENT_KEYWORDS = [
    "conference",
    "summit",
    "meetup",
    "workshop",
    "ux",
    "design",
    "research"
]

EXCLUDE_KEYWORDS = [
    "course",
    "training",
    "degree",
    "diploma",
    "bootcamp",
    "job",
    "hiring",
]


def verify_event(title):

    text = title.lower()

    if any(bad in text for bad in EXCLUDE_KEYWORDS):
        return False

    score = 0

    for word in EVENT_KEYWORDS:
        if word in text:
            score += 1

    return score >= 2