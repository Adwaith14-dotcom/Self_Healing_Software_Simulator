import streamlit as st

DEFAULT_SETTINGS = {
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
    "anonymize_logs": False,
    "email_user": "",
    "gmail_app_password": "",
    "email_recipient": ""
}


def ensure_settings():
    for key, default_value in DEFAULT_SETTINGS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def show_settings_page():
    ensure_settings()

    st.header("⚙️ Control Center & Configuration")
    st.markdown(
        "Customize monitoring thresholds, notification behavior, and dashboard style to match your environment."
    )

    with st.expander("System Thresholds", expanded=True):
        cpu_val = st.slider(
            "CPU Alert Threshold (%)",
            50,
            100,
            st.session_state.cpu_threshold
        )
        st.session_state.cpu_threshold = cpu_val
        
        mem_val = st.slider(
            "Memory Alert Threshold (%)",
            50,
            100,
            st.session_state.mem_threshold
        )
        st.session_state.mem_threshold = mem_val
        
        disk_val = st.slider(
            "Disk Alert Threshold (%)",
            50,
            100,
            st.session_state.disk_threshold
        )
        st.session_state.disk_threshold = disk_val

    with st.expander("Appearance", expanded=False):
        theme_val = st.radio(
            "Dashboard Theme",
            ["Light", "Dark"],
            index=["Light", "Dark"].index(st.session_state.theme)
        )
        st.session_state.theme = theme_val
        
        gauge_val = st.radio(
            "Gauge Style",
            ["Colorful", "Minimal"],
            index=["Colorful", "Minimal"].index(st.session_state.gauge_style)
        )
        st.session_state.gauge_style = gauge_val

    with st.expander("Notifications", expanded=False):
        notify_val = st.selectbox(
            "Alert Style",
            ["Pop-up", "Banner", "Silent Log"],
            index=["Pop-up", "Banner", "Silent Log"].index(st.session_state.notify_mode)
        )
        st.session_state.notify_mode = notify_val
        
        auto_heal_val = st.checkbox(
            "Enable Auto-Healing Actions",
            value=st.session_state.auto_heal
        )
        st.session_state.auto_heal = auto_heal_val

        st.write("Email alerts are sent automatically for critical errors.")
        st.write("Use environment variables or root email_config.json for credentials; no manual typing is required.")

        if st.session_state.email_user and st.session_state.gmail_app_password and st.session_state.email_recipient:
            st.write("✅ Email alerting is configured.")
        else:
            st.write("⚠️ Email alerting is not configured. Set EMAIL_USER, GMAIL_APP_PASSWORD, and EMAIL_RECIPIENT in the environment or email_config.json.")

    with st.expander("Data & Logs", expanded=False):
        export_val = st.selectbox(
            "Default Export Format",
            ["CSV", "Excel", "JSON"],
            index=["CSV", "Excel", "JSON"].index(st.session_state.export_format)
        )
        st.session_state.export_format = export_val
        
        retention_val = st.number_input(
            "Log Retention (days)",
            min_value=1,
            max_value=30,
            value=st.session_state.retention
        )
        st.session_state.retention = retention_val

    with st.expander("System Refresh", expanded=False):
        refresh_val = st.selectbox(
            "Refresh Interval (seconds)",
            [2, 5, 10, 30],
            index=[2, 5, 10, 30].index(st.session_state.refresh_rate)
        )
        st.session_state.refresh_rate = refresh_val

    with st.expander("Security", expanded=False):
        pwd_val = st.checkbox(
            "Enable Password Protection",
            value=st.session_state.password_protect
        )
        st.session_state.password_protect = pwd_val
        
        anon_val = st.checkbox(
            "Anonymize Logs Before Export",
            value=st.session_state.anonymize_logs
        )
        st.session_state.anonymize_logs = anon_val

    col1, col2 = st.columns([3, 2])
    with col1:
        st.write("✅ Settings applied to the session.")
        st.write("These values are now stored and will be used by the dashboard for behavior, alerts, and appearance.")
    with col2:
        st.metric("Auto-Healing", "Enabled" if st.session_state.auto_heal else "Disabled")
        st.metric("Theme", st.session_state.theme)
        st.metric("Refresh", f"{st.session_state.refresh_rate}s")

    if st.button("Reset to defaults"):
        for key, val in DEFAULT_SETTINGS.items():
            st.session_state[key] = val
        st.rerun()
