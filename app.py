import sys, os
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")

import streamlit as st
import pandas as pd
import threading
import time
from streamlit_autorefresh import st_autorefresh

sys.path.append(os.path.dirname(__file__))

from upgrades.sidebar import show_sidebar
from system_monitor import show_monitoring_section
from debugger.viewer import show_debugger_section
from tools.tools_viewer import show_tools_section
from home import show_home_page
from settings import show_settings_page
from loading import show_loading_screen

from engine import run_engine, metrics_queue
from web_monitor.capture import check_login, check_booking, capture_queue
from web_monitor.error_manager import resolve_error
from web_monitor.notifications import (
    send_email_notification,
    send_slack_notification,
    send_desktop_notification,
    capture_screenshot,
    load_email_config
)
from web_monitor.auto_resolver import auto_resolve
from web_monitor.demo_site import load_demo_events

st.set_page_config(page_title="Self-Healing Monitoring Dashboard", layout="wide")

def ensure_session_key(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

APP_ROOT = Path(__file__).resolve().parent
LOG_FILE = APP_ROOT / "system_bugs.log"

defaults = {
    "loaded": False,
    "metric_history": pd.DataFrame(columns=["CPU", "Memory", "Disk", "Timestamp"]),
    "engine_started": False,
    "capture_watcher_started": False,
    "demo_event_watcher_started": False,
    "errors": [],
    "success": [],
    "resolved": [],
    "auto_resolved": [],
    "all_events": [],
    "function_checks": [],
    "cpu_threshold": 80,
    "mem_threshold": 75,
    "disk_threshold": 85,
    "theme": "Dark",
    "gauge_style": "Colorful",
    "notify_mode": "Pop-up",
    "auto_heal": True,
    "export_format": "CSV",
    "retention": 7,
    "refresh_rate": 5,
    "password_protect": False,
    "anonymize_logs": False
}

for key, value in defaults.items():
    ensure_session_key(key, value)

email_config = load_email_config()
st.session_state["email_user"] = os.getenv("EMAIL_USER", email_config.get("EMAIL_USER", st.session_state.get("email_user", "adwth1369@gmail.com")))
st.session_state["gmail_app_password"] = os.getenv("GMAIL_APP_PASSWORD", email_config.get("GMAIL_APP_PASSWORD", st.session_state.get("gmail_app_password", "tkyu pnxb gvve mpco")))
st.session_state["email_recipient"] = os.getenv("EMAIL_RECIPIENT", email_config.get("EMAIL_RECIPIENT", st.session_state.get("email_recipient", "adwaithr165@gmail.com")))
if "email_status" not in st.session_state:
    st.session_state["email_status"] = "Email alerting will send automatically when configured."

if not st.session_state["engine_started"]:
    threading.Thread(target=run_engine, daemon=True).start()
    st.session_state["engine_started"] = True

if "demo_event_watcher_started" not in st.session_state:
    st.session_state["demo_event_watcher_started"] = False


def record_function_check(event):
    st.session_state["function_checks"].append(
        {
            "Site": event.get("Site", "Unknown"),
            "Action": event["Type"],
            "Status": "PASS" if event["Severity"] in ["Info", "Resolved"] else "FAIL",
            "Message": event["Message"],
            "Remedy": event.get("Remedy", "Review the issue and retry."),
            "Severity": event["Severity"],
            "Timestamp": event["Timestamp"]
        }
    )


def derive_remedy(event):
    remedies = {
        "Login Error": "Retry login with a fresh session and validate credentials.",
        "Login Exception": "Check the authentication service or network, then rerun login.",
        "Booking Error": "Retry booking after refreshing the session or clearing temporary state.",
        "Booking Exception": "Verify the booking endpoint and network access, then retry.",
        "HighCPU": "Close unused applications or scale resources to reduce CPU load.",
        "HighMemory": "Free memory by restarting heavy services or clearing caches.",
        "Disk Space Critical": "Delete unnecessary files or expand disk capacity.",
    }
    return remedies.get(event.get("Type"), "Review the failure details and retry the affected service.")


def attempt_auto_remedy(event):
    if not st.session_state.get("auto_heal", False):
        return

    if event.get("Type") in ["Login Error", "Login Exception"]:
        check_login()
        process_capture_events()
    elif event.get("Type") in ["Booking Error", "Booking Exception"]:
        check_booking()
        process_capture_events()


def process_error_event(event):
    print("📥 Event received:", event)

    event["Remedy"] = derive_remedy(event)
    st.session_state["all_events"].append(event)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{event['Timestamp']} - {event['Site']} - {event['Type']} - {event['Message']} - {event['Severity']}\n")

    if event["Severity"] in ["Critical", "High", "Warning"] or event["Category"].lower().endswith("error"):
        st.session_state["errors"].append(event)

        screenshot_file = capture_screenshot()
        email_subject = f"🚨 System Alert: {event['Type']} on {event.get('Site', 'System')}"
        email_details = f"""
System Alert Detected:
- Site: {event.get('Site', 'Unknown')}
- Type: {event['Type']}
- Message: {event['Message']}
- Category: {event['Category']}
- Timestamp: {event['Timestamp']}
- Severity: {event['Severity']}
- Remedy: {event['Remedy']}

This event was automatically detected and logged.
A screenshot has been captured and attached when available.
Please review the attached system_bugs.log for additional context.
"""

        email_sent = send_email_notification(
            subject=email_subject,
            body=email_details,
            recipient=st.session_state["email_recipient"],
            sender_email=st.session_state["email_user"],
            app_password=st.session_state["gmail_app_password"],
            screenshot_file=screenshot_file
        )
        st.session_state["email_status"] = "Email sent successfully." if email_sent else "Email failed. Check credentials and network."
        send_slack_notification(
            f"{event.get('Site', 'Unknown')} - {event['Type']} - {event['Message']} at {event['Timestamp']}\nScreenshot saved: {screenshot_file}",
            severity="Critical"
        )
        send_desktop_notification(
            "Critical Site Error Detected",
            f"{event.get('Site', 'Unknown')} - {event['Type']}"
        )

        if st.session_state.get("auto_heal", False):
            attempt_auto_remedy(event)

        resolution_message = auto_resolve(event["Type"], event["Message"])
        st.session_state["auto_resolved"].append({
            "Category": event["Category"],
            "Type": event["Type"],
            "Message": event["Message"],
            "ResolutionMessage": resolution_message,
            "Timestamp": pd.Timestamp.now()
        })

    elif event["Severity"] == "Resolved":
        st.session_state["resolved"].append({
            **event,
            "ResolutionMessage": event["Message"],
            "ResolvedAt": pd.Timestamp.now()
        })
    else:
        st.session_state["success"].append(event)

    if event["Category"].startswith("Web"):
        record_function_check(event)


def process_capture_events():
    while not capture_queue.empty():
        event = capture_queue.get()
        process_error_event(event)


def capture_event_watcher():
    while True:
        process_capture_events()
        time.sleep(1)


def run_full_function_checks():
    st.session_state["function_checks"] = []
    check_login()
    process_capture_events()
    check_booking()
    process_capture_events()
    st.success("✅ Full system function check completed. See the latest site and function results below.")


def process_demo_events():
    events = load_demo_events()
    if not events:
        return

    for event in events:
        process_error_event(event)

    st.session_state["last_demo_event_processed"] = {
        "count": len(events),
        "timestamp": pd.Timestamp.now(),
        "last_type": events[-1].get("Type", "Unknown")
    }


def demo_event_watcher():
    while True:
        process_demo_events()
        time.sleep(3)


if not st.session_state["capture_watcher_started"]:
    threading.Thread(target=capture_event_watcher, daemon=True).start()
    st.session_state["capture_watcher_started"] = True

if not st.session_state["demo_event_watcher_started"]:
    threading.Thread(target=demo_event_watcher, daemon=True).start()
    st.session_state["demo_event_watcher_started"] = True

if not st.session_state["loaded"]:
    show_loading_screen()
else:
    section = show_sidebar()

    if "Home" in section:
        show_home_page()

    elif "Monitoring Window" in section:
        st.header("📊 Monitoring Window")
        while not metrics_queue.empty():
            new_row = metrics_queue.get()
            st.session_state["metric_history"] = pd.concat(
                [st.session_state["metric_history"], pd.DataFrame([new_row])],
                ignore_index=True
            )
        show_monitoring_section()

    elif "Settings" in section:
        show_settings_page()

    elif "Logs" in section:
        sub_tab = st.sidebar.radio("History Options", ["Validation History", "Routing History", "System Bugs"])
        log_lines = []
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_lines = [line.strip() for line in f if line.strip()]

        if sub_tab == "Validation History":
            if log_lines:
                st.subheader("Validation History")
                st.dataframe(pd.DataFrame({"Log": log_lines[-20:]}), width="stretch")
            else:
                st.write("No validation logs yet.")
        elif sub_tab == "Routing History":
            st.write("Routing history will be displayed here.")
        else:
            if log_lines:
                st.subheader("System Bugs Detected")
                st.dataframe(pd.DataFrame({"Log": log_lines[-20:]}), width="stretch")
            else:
                st.write("No system bugs logged yet.")

    elif "Debugger" in section:
        st.header("🪲 Debugger Window")
        errors = []
        show_debugger_section(errors)

    elif "Tools" in section:
        st.header("🛡️ Tools")
        show_tools_section()

    elif "Error Monitor" in section:
        st.header("🛠️ Error Monitor & Site Health")

        if "refresh_rate" not in st.session_state:
            st.session_state["refresh_rate"] = 5

        st.markdown("### 🔧 Full System Function & Site Health Check")
        st.write(
            "Live site and generated demo events are monitored automatically across all configured sources. "
            "The dashboard refreshes continuously to surface new errors, usage events, and remediation alerts."
        )

        st_autorefresh(interval=st.session_state["refresh_rate"] * 1000, key="error_monitor_autorefresh")
        process_capture_events()
        process_demo_events()

        status_col1, status_col2, status_col3, status_col4 = st.columns(4)
        status_col1.metric("Active Errors", len(st.session_state["errors"]))
        status_col2.metric("Successful Events", len(st.session_state["success"]))
        status_col3.metric("Resolved Issues", len(st.session_state["resolved"]))
        status_col4.metric("Auto-Resolved", len(st.session_state["auto_resolved"]))

        demo_info = st.session_state.get("last_demo_event_processed", {})
        st.markdown(
            f"**Total events processed:** {len(st.session_state['all_events'])}  \
            **Last event:** {demo_info.get('last_type', 'None')}  \
            **Processed at:** {demo_info.get('timestamp', 'N/A')}"
        )
        email_status = "Configured" if (st.session_state["email_user"] and st.session_state["gmail_app_password"] and st.session_state["email_recipient"]) else "Not configured"
        st.write(f"Email status: {email_status} — {st.session_state['email_status']}")
        if email_status == "Configured":
            st.write(f"Sending from: `{st.session_state['email_user']}` to `{st.session_state['email_recipient']}`")
        else:
            st.warning("Email credentials are not fully configured. Set EMAIL_USER, GMAIL_APP_PASSWORD, and EMAIL_RECIPIENT in the environment or email_config.json.")

        if st.button("🔄 Refresh Monitor"):
            process_capture_events()
            process_demo_events()
            st.experimental_rerun() # type: ignore

        if st.button("🔍 Run full simulator health check"):
            run_full_function_checks()

        if st.session_state["function_checks"]:
            st.subheader("📋 Recent Site & Function Results")
            df_checks = pd.DataFrame(st.session_state["function_checks"])
            if len(df_checks) > 0:
                st.dataframe(
                    df_checks,
                    use_container_width=True,
                    column_config={
                        "Site": st.column_config.TextColumn("Site Name", width="medium"),
                        "Action": st.column_config.TextColumn("Function/Action", width="medium"),
                        "Status": st.column_config.TextColumn("Status", width="small"),
                        "Remedy": st.column_config.TextColumn("Remedy Steps", width="large"),
                        "Severity": st.column_config.TextColumn("Severity", width="small"),
                    }
                )

        if st.session_state["errors"]:
            st.subheader("⚠️ Active Errors with Remedy Steps")
            df_errors = pd.DataFrame(st.session_state["errors"])
            if len(df_errors) > 0:
                st.dataframe(
                    df_errors,
                    use_container_width=True,
                    column_config={
                        "Site": st.column_config.TextColumn("Site", width="medium"),
                        "Type": st.column_config.TextColumn("Error Type", width="medium"),
                        "Message": st.column_config.TextColumn("Issue", width="large"),
                        "Remedy": st.column_config.TextColumn("How to Fix", width="large"),
                        "Severity": st.column_config.TextColumn("Severity", width="small"),
                    }
                )
        else:
            st.write("✅ No active errors. Run the full health check to validate system functions and logged-in sites.")

        if st.session_state["success"]:
            df_success = pd.DataFrame(st.session_state["success"])
            st.subheader("✅ Successful Actions")
            st.dataframe(df_success, width="stretch")

        if st.session_state["resolved"]:
            df_resolved = pd.DataFrame(st.session_state["resolved"])
            df_resolved["Severity"] = "🟢 Resolved"
            st.subheader("🟢 Resolved Issues")
            st.dataframe(df_resolved, width="stretch")

        if st.session_state["auto_resolved"]:
            df_auto = pd.DataFrame(st.session_state["auto_resolved"])
            df_auto["Severity"] = "🛠️ Auto-Resolved"
            st.subheader("🛠️ Auto-Resolved Issues")
            st.dataframe(
                df_auto[
                    ["Category", "Type", "Message", "ResolutionMessage", "Severity", "Timestamp"]
                ].style.apply(
                    lambda row: ["background-color: #e0ffe0"] * len(row),
                    axis=1
                ),
                width="stretch"
            )

