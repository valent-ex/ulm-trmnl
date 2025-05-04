import requests

def send_payload(webhook, payload):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(webhook, json=payload, headers=headers)
        response.raise_for_status()
        print(f"✅ Sent to {webhook}")
    except Exception as e:
        print(f"❌ Failed to send to {webhook}: {e}")
