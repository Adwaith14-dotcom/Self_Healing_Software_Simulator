import smtplib
import os
import time
import requests
import pyautogui
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_desktop_notification(title: str, message: str):
    """Show a Windows toast notification."""
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=10, threaded=True)
        while toaster.notification_active():
            time.sleep(0.1)
        print("✅ Desktop notification sent")
    except ImportError:
        print("❌ win10toast not installed")
    except Exception as e:
        print(f"❌ Desktop notification failed: {e}")

def capture_screenshot(filename: str = "error_screenshot.png") -> str | None:
    """Capture a screenshot of the current screen."""
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"✅ Screenshot saved as {filename}")
        return filename
    except Exception as e:
        print(f"❌ Failed to capture screenshot: {e}")
        return None

def send_email_notification(subject: str, body: str, to_email: str, screenshot_file: str | None = None):
    """
    Sends an email notification using Gmail SMTP.
    Requires a Gmail App Password stored in environment variable GMAIL_APP_PASSWORD.
    """
    sender_email = os.getenv("EMAIL_USER", "adwth1369@gmail.com")
    app_password = os.getenv("GMAIL_APP_PASSWORD", "your-app-password-here")

    print("📧 Preparing to send email...")
    print(f"   Subject: {subject}")
    print(f"   To: {to_email}")

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.attach(MIMEText(body, "plain"))

    if screenshot_file and os.path.exists(screenshot_file):
        try:
            with open(screenshot_file, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(screenshot_file)}")
            msg.attach(part)
            print(f"   ✅ Attached screenshot: {screenshot_file}")
        except Exception as e:
            print(f"   ❌ Failed to attach screenshot: {e}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            print("   🔑 Logging in to Gmail SMTP...")
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_slack_notification(message: str, severity: str = "Info"):
    """Send a Slack alert via webhook."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/XXXX/XXXX/XXXX")
    payload = {"text": f"{severity} Alert: {message}"}
    try:
        requests.post(webhook_url, json=payload)
        print("✅ Slack notification sent")
    except Exception as e:
        print(f"❌ Failed to send Slack notification: {e}")
