"""
Test script for email notification system.
Sets up environment variables and tests email functionality.
"""

import os
import sys
from web_monitor.notifications import send_email_notification, capture_screenshot, ensure_email_config

def setup_email_config():
    """Configure email environment variables."""
    print("📧 Setting up email configuration...")
    
    default_config = {
        "EMAIL_USER": "adwth1369@gmail.com",
        "GMAIL_APP_PASSWORD": "tkyu pnxb gvve mpco",
        "EMAIL_RECIPIENT": "adwaithr165@gmail.com"
    }
    
    for key, default_value in default_config.items():
        value = os.getenv(key) or default_value
        os.environ[key] = value
        status = "✅" if os.getenv(key) else "❌"
        print(f"   {status} {key}: {value[:20]}...")
    
    return ensure_email_config()

def test_email():
    """Test email notification with screenshot."""
    print("\n🧪 Testing email notification system...\n")
    
    print("📸 Capturing screenshot...")
    screenshot = capture_screenshot("test_error_screenshot.png")
    
    print("\n📨 Sending test email with details...")
    body = """
TEST EMAIL NOTIFICATION
=======================

This is a test email from your Self-Healing Streamlit application.

✅ Email system is working correctly!
✅ Screenshots are being attached
✅ Error details are included
✅ System logs are attached

If you received this email, your alert system is properly configured.
    """
    
    success = send_email_notification(
        subject="✅ Test: Email Notification System Working",
        body=body,
        screenshot_file=screenshot
    )
    
    return success

if __name__ == "__main__":
    print("=" * 50)
    print("   EMAIL NOTIFICATION SYSTEM TEST")
    print("=" * 50 + "\n")
    
    config_ok = setup_email_config()
    
    if not config_ok:
        print("\n❌ Email configuration failed!")
        print("\nTo fix this, set environment variables:")
        print("   $env:EMAIL_USER = 'your_gmail@gmail.com'")
        print("   $env:GMAIL_APP_PASSWORD = 'your_app_password'")
        print("   $env:EMAIL_RECIPIENT = 'recipient@email.com'")
        sys.exit(1)
    
    print("\n" + "=" * 50 + "\n")
    success = test_email()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Email test completed successfully!")
        print("   Your error notification system is ready.")
    else:
        print("❌ Email test failed!")
        print("   Check your credentials and try again.")
    print("=" * 50)
