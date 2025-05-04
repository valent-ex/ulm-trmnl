import os

TASKS = [
    {
        "name": "trash",
        "interval": int(os.getenv("TRASH_INTERVAL", "86400")),
        "handler": "services.trash.generate_payload",
        "webhook": os.getenv("TRASH_WEBHOOK")
    }
]
