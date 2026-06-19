import csv
import json

def export_logs_csv(logs, filename="logs.csv"):
    """Export logs to CSV file."""
    keys = logs[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(logs)

def export_logs_json(logs, filename="logs.json"):
    """Export logs to JSON file."""
    with open(filename, "w") as f:
        json.dump(logs, f, indent=4)