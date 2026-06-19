import json
import smtplib
import os
import time
import requests
import pyautogui
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "email_config.json"
ENV_FILE = PROJECT_ROOT / ".env"
_last_email_error = ""

def ensure_email_config():
    """Ensure required email environment variables are set."""
    required_vars = ["EMAIL_USER", "GMAIL_APP_PASSWORD", "EMAIL_RECIPIENT"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"⚠️  Warning: Missing email config variables: {', '.join(missing)}")
        print("   Email notifications will not work. Set them with:")
        for var in missing:
            print(f"   $env:{var} = 'your_value'")
        return False
    return True


def load_email_config():
    config = {}
    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"❌ Failed to parse {CONFIG_FILE}: {e}")

    if ENV_FILE.exists():
        try:
            for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
                if not line.strip() or line.strip().startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                config.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        except Exception as e:
            print(f"❌ Failed to parse {ENV_FILE}: {e}")

    return config


def get_last_email_error() -> str:
    return _last_email_error

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


def send_email_notification(subject: str, body: str, recipient: str | None = None, sender_email: str | None = None, app_password: str | None = None, screenshot_file: str | None = None):
    """
    Sends an email notification using Gmail SMTP.
    Uses values from function arguments, environment variables, or config file.
    """
    config = load_email_config()
    sender_email = sender_email or os.getenv("EMAIL_USER") or config.get("EMAIL_USER")
    app_password = app_password or os.getenv("GMAIL_APP_PASSWORD") or config.get("GMAIL_APP_PASSWORD")
    recipient = recipient or os.getenv("EMAIL_RECIPIENT") or config.get("EMAIL_RECIPIENT")

    global _last_email_error
    if not sender_email or not app_password or not recipient:
        _last_email_error = "Email credentials not configured. Set EMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_RECIPIENT, or email_config.json"
        print("❌ Email credentials not configured. Cannot send email.")
        print("   Set environment variables: EMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_RECIPIENT, or use email_config.json")
        print(f"   sender_email={sender_email}, recipient={recipient}, app_password_provided={bool(app_password)}")
        return False

    print("📧 Preparing to send email...")
    print(f"   Subject: {subject}")
    print(f"   To: {recipient}")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #d32f2f;">⚠️ System Alert</h2>
            <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr style="border: 1px solid #ccc;">
            <p>{body}</p>
            <hr style="border: 1px solid #ccc;">
            <p style="color: #666; font-size: 12px;">This is an automated alert from your Self-Healing Streamlit application.</p>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

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

    log_file = PROJECT_ROOT / "system_bugs.log"
    if log_file.exists():
        try:
            with open(log_file, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={log_file.name}")
            msg.attach(part)
            print(f"   ✅ Attached log file: {log_file}")
        except Exception as e:
            print(f"   ❌ Failed to attach log file: {e}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            print("   🔑 Logging in to Gmail SMTP...")
            server.login(sender_email, app_password)
            server.send_message(msg)
        _last_email_error = ""
        print("✅ Email sent successfully")
        return True
    except smtplib.SMTPAuthenticationError:
        _last_email_error = "Gmail authentication failed. Check EMAIL_USER and GMAIL_APP_PASSWORD."
        print("❌ Gmail authentication failed. Check EMAIL_USER and GMAIL_APP_PASSWORD.")
        return False
    except Exception as e:
        _last_email_error = f"Failed to send email: {e}"
        print(f"❌ Failed to send email: {e}")
        return False

def send_slack_notification(message: str, severity: str = "Info"):
    """Send a Slack alert via webhook."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/XXXX/XXXX/XXXX")
    payload = {"text": f"{severity} Alert: {message}"}
    try:
        requests.post(webhook_url, json=payload)
        print("✅ Slack notification sent")
    except Exception as e:
        print(f"❌ Failed to send Slack notification: {e}")
