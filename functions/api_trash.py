import json
import requests
from ics import Calendar
from datetime import datetime, date
import os

TYPE_MAP = {
    "Restmüll": "REST",
    "Biotonne": "BIO",
    "Blaue Tonne": "BLAU",
    "Gelber Sack": "GELB"
}

_cached_calendar = None
_cached_date = None

def get_cached_calendar():
    global _cached_calendar, _cached_date
    today = date.today()
    if _cached_calendar is None or _cached_date != today:
        bezirk = os.getenv("BEZIRK", "10")
        url = f"https://www.ebu-ulm.de/export.php?bezirk={bezirk}&jahr={today.year}"
        response = requests.get(url)
        _cached_calendar = Calendar(response.text)
        _cached_date = today
    return _cached_calendar

def handler(event, context):
    calendar = get_cached_calendar()
    today = datetime.now().date()
    trash = {}

    for event in calendar.events:
        dt = event.begin.date()
        kind = event.name.strip()

        if kind not in TYPE_MAP:
            continue

        if dt >= today:
            label = TYPE_MAP[kind]
            trash.setdefault(label, []).append(dt)

    result = {}
    for kind, dates in trash.items():
        dates.sort()
        nearest = dates[0].strftime("%d.%m")
        next_one = dates[1].strftime("%d.%m") if len(dates) > 1 else None
        result[f"{kind.lower()}_next"] = nearest
        result[f"{kind.lower()}_after_next"] = next_one

    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps(result)
    }
