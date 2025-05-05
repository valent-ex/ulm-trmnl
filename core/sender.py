import requests
import sys

def send_payload(webhook, payload):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(webhook, json=payload, headers=headers)
        response.raise_for_status()
        sys.stdout.write(f"✅ Sent to {webhook}\n")
        sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(f"❌ Failed to send to {webhook}: {e}\n")
        sys.stderr.flush()
