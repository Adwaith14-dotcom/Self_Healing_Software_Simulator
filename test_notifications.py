from web_monitor.notifications import (
    send_email_notification,
    send_slack_notification,
    send_desktop_notification
)

send_email_notification("Test Alert", "This is a test email", "adwth1369@gmail.com")

send_slack_notification("This is a test Slack alert", severity="Info")

send_desktop_notification("Test Pop-up", "This is a desktop notification")
