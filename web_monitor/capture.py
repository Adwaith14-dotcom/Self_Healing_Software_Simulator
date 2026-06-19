import requests
import time
import queue
import pandas as pd

# Shared queue for capture results
capture_queue = queue.Queue()

MAX_RETRIES = 3
COOLDOWN = 5  # seconds between retries

def check_login():
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            response = requests.post("http://127.0.0.1:5000/login")
            data = response.json()
            if data["status"] == "error":
                attempts += 1
                if attempts < MAX_RETRIES:
                    time.sleep(COOLDOWN)
                    continue
                else:
                    capture_queue.put({
                        "Category": "Web Error",
                        "Type": "Login Error",
                        "Message": data["message"],
                        "Severity": "Critical",
                        "Timestamp": pd.Timestamp.now()
                    })
                    return
            else:
                site_name = "Authentication Service"
                if attempts > 0:
                    capture_queue.put({
                        "Category": "Web Error",
                        "Site": site_name,
                        "Type": "Login Error",
                        "Message": "Recovered after retry",
                        "Severity": "Resolved",
                        "Timestamp": pd.Timestamp.now()
                    })
                capture_queue.put({
                    "Category": "Web Success",
                    "Site": site_name,
                    "Type": "Login Success",
                    "Message": data["message"],
                    "Severity": "Info",
                    "Timestamp": pd.Timestamp.now()
                })
                return
        except Exception as e:
            attempts += 1
            if attempts < MAX_RETRIES:
                time.sleep(COOLDOWN)
                continue
            else:
                capture_queue.put({
                    "Category": "Web Error",
                    "Site": "Authentication Service",
                    "Type": "Login Exception",
                    "Message": str(e),
                    "Severity": "Critical",
                    "Timestamp": pd.Timestamp.now()
                })
                return

def check_booking():
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            response = requests.post("http://127.0.0.1:5000/book")
            data = response.json()
            if data["status"] == "error":
                attempts += 1
                if attempts < MAX_RETRIES:
                    time.sleep(COOLDOWN)
                    continue
                else:
                    capture_queue.put({
                        "Category": "Web Error",
                        "Type": "Booking Error",
                        "Message": data["message"],
                        "Severity": "Critical",
                        "Timestamp": pd.Timestamp.now()
                    })
                    return
            else:
                site_name = "Booking Service"
                if attempts > 0:
                    capture_queue.put({
                        "Category": "Web Error",
                        "Site": site_name,
                        "Type": "Booking Error",
                        "Message": "Recovered after retry",
                        "Severity": "Resolved",
                        "Timestamp": pd.Timestamp.now()
                    })
                capture_queue.put({
                    "Category": "Web Success",
                    "Site": site_name,
                    "Type": "Booking Success",
                    "Message": data["message"],
                    "Severity": "Info",
                    "Timestamp": pd.Timestamp.now()
                })
                return
        except Exception as e:
            attempts += 1
            if attempts < MAX_RETRIES:
                time.sleep(COOLDOWN)
                continue
            else:
                capture_queue.put({
                    "Category": "Web Error",
                    "Site": "Booking Service",
                    "Type": "Booking Exception",
                    "Message": str(e),
                    "Severity": "Critical",
                    "Timestamp": pd.Timestamp.now()
                })
                return
