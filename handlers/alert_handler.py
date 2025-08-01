import json
import os

ALERT_FILE = "alerts.json"

def save_alerts_to_file():
    try:
        with open(ALERT_FILE, "w") as f:
            json.dump(alerts, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Saving alerts: {e}")

def load_alerts_from_file():
    global alerts
    if os.path.exists(ALERT_FILE):
        try:
            with open(ALERT_FILE, "r") as f:
                alerts = json.load(f)
        except Exception as e:
            print(f"[ERROR] Loading alerts: {e}")
