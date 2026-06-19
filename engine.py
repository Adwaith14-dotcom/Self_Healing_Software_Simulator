import psutil
import time
import logging
import pandas as pd
import queue
import warnings
from web_monitor.notifications import send_email_notification, capture_screenshot, ensure_email_config

warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")

logging.basicConfig(
    filename="system_bugs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

metrics_queue = queue.Queue()

def get_safe_value(value) -> float:
    if isinstance(value, list):
        return float(value[0]) if value else 0.0
    elif isinstance(value, (int, float)):
        return float(value)
    else:
        return 0.0

def run_engine() -> None:
    """Background engine that continuously monitors system health."""
    while True:
        cpu = get_safe_value(psutil.cpu_percent(interval=1, percpu=False))
        mem = get_safe_value(psutil.virtual_memory().percent)
        disk = get_safe_value(psutil.disk_usage('/').percent)
        ts = pd.Timestamp.now()

        if cpu > 90.0:
            logging.error(f"High CPU detected: {cpu}%")
            screenshot = capture_screenshot()
            body = f"""
HIGH CPU USAGE ALERT
====================
Current CPU Usage: {cpu:.2f}%
Threshold: 90%
Timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}

⚠️ Your system is experiencing high CPU usage.
Please check running processes and close unnecessary applications.
Screenshot of the system is attached for your reference.
            """
            send_email_notification(
                subject=f"🔴 CRITICAL: High CPU Usage Alert - {cpu:.2f}%",
                body=body,
                screenshot_file=screenshot
            )

        if mem > 80.0:
            logging.error(f"High Memory usage detected: {mem}%")
            screenshot = capture_screenshot()
            body = f"""
HIGH MEMORY USAGE ALERT
=======================
Current Memory Usage: {mem:.2f}%
Threshold: 80%
Timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}

⚠️ Your system is running low on memory.
Consider closing unnecessary applications or restarting your system.
Screenshot of the system is attached for your reference.
            """
            send_email_notification(
                subject=f"🟡 WARNING: High Memory Usage Alert - {mem:.2f}%",
                body=body,
                screenshot_file=screenshot
            )

        if disk > 90.0:
            logging.error(f"Disk almost full: {disk}%")
            screenshot = capture_screenshot()
            body = f"""
DISK SPACE CRITICAL ALERT
=========================
Current Disk Usage: {disk:.2f}%
Threshold: 90%
Timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}

🔴 Your disk is almost full!
Please free up disk space immediately.
Screenshot of the system is attached for your reference.
            """
            send_email_notification(
                subject=f"🔴 CRITICAL: Disk Space Critical Alert - {disk:.2f}%",
                body=body,
                screenshot_file=screenshot
            )

        logging.info(f"System OK - CPU: {cpu}%, Memory: {mem}%, Disk: {disk}%")

        metrics_queue.put({"CPU": cpu, "Memory": mem, "Disk": disk, "Timestamp": ts})

        time.sleep(5)
