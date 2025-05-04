from ics import Calendar
from datetime import datetime, date, timedelta
import requests
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
        bezirk = os.getenv("TRASH_BEZIRK", "10")
        url = f"https://www.ebu-ulm.de/export.php?bezirk={bezirk}&jahr={today.year}"
        response = requests.get(url)
        _cached_calendar = Calendar(response.text)
        _cached_date = today
    return _cached_calendar

def generate_payload():
    calendar = get_cached_calendar()
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    trash = {}

    for event in calendar.events:
        dt = event.begin.date()
        kind = event.name.strip()
        if kind not in TYPE_MAP or dt < today:
            continue
        label = TYPE_MAP[kind]
        trash.setdefault(label, []).append(dt)

    result = {
        "today": today.strftime("%d.%m"),
        "today_day": today.strftime("%a")[:2]
    }

    for kind, dates in trash.items():
        dates.sort()
        next_dt = dates[0]
        next_one_dt = dates[1] if len(dates) > 1 else None

        key = kind.lower()
        result[f"{key}_next"] = next_dt.strftime("%d.%m")
        result[f"{key}_next_day"] = next_dt.strftime("%a")[:2]
        result[f"{key}_is_today"] = next_dt == today
        result[f"{key}_is_tomorrow"] = next_dt == tomorrow

        if next_one_dt:
            result[f"{key}_after_next"] = next_one_dt.strftime("%d.%m")

    return { "merge_variables": result }
