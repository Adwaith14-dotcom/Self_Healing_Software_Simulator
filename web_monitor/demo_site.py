import json
import time
from pathlib import Path

DEMO_EVENT_FILE = Path(__file__).resolve().parent.parent / "demo_events.jsonl"


def generate_demo_error(error_type):
    demo_errors = {
        "LoginError": {
            "Site": "Authentication Service",
            "Category": "Web Error",
            "Message": "Login failed due to invalid session",
            "Severity": "Critical"
        },
        "ServiceCrash": {
            "Site": "Background Service",
            "Category": "System Error",
            "Message": "Background service crashed unexpectedly",
            "Severity": "Critical"
        },
        "HighCPU": {
            "Site": "System Monitor",
            "Category": "System Error",
            "Message": "CPU usage exceeded 95%",
            "Severity": "High"
        },
        "MinorWarning": {
            "Site": "Cache Manager",
            "Category": "App Error",
            "Message": "Cache not cleared properly",
            "Severity": "Warning"
        },
        "InfoEvent": {
            "Site": "System Monitor",
            "Category": "App Info",
            "Message": "Routine check completed successfully",
            "Severity": "Info"
        }
    }

    error = demo_errors.get(error_type, {
        "Category": "Unknown",
        "Message": "Unknown error type",
        "Severity": "Unknown"
    })
    error["Type"] = error_type
    error["Timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    return error


def save_demo_event(event):
    DEMO_EVENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DEMO_EVENT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def load_demo_events():
    if not DEMO_EVENT_FILE.exists():
        return []

    with open(DEMO_EVENT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    events = []
    for line in lines:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    open(DEMO_EVENT_FILE, "w", encoding="utf-8").close()
    return events
