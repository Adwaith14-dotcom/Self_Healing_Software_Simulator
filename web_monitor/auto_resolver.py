import os
import subprocess
from web_monitor.notifications import send_desktop_notification

def auto_resolve(error_type, error_message):
    """
    Attempts to automatically resolve known error types.
    Returns a resolution message string.
    """

    if error_type == "LoginError":
        send_desktop_notification("Auto-Resolution", "Retrying login...")
        return "Login retried automatically"

    elif error_type == "ServiceCrash":
        send_desktop_notification("Auto-Resolution", "Restarting service...")
        try:
            subprocess.run(["systemctl", "restart", "myservice"])
            return "Service restarted"
        except Exception:
            return "Failed to restart service"

    elif error_type == "HighCPU":
        send_desktop_notification("Auto-Resolution", "Killing heavy process...")
        os.system("taskkill /F /IM chrome.exe")  
        return "Process killed"

    else:
        return "No auto-resolution available"
