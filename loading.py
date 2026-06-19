import streamlit as st
import time

def show_loading_screen():
    st.markdown(
        """
        <div style='text-align:center; margin-top:80px; font-family:Segoe UI, sans-serif;'>
            <h1 style='color:#1f2937; letter-spacing:0.05em; margin-bottom:4px;'>Self-Healing Software Simulator</h1>
            <p style='color:#475569; font-size:16px; margin:0 auto; max-width:700px;'>A professional monitoring workspace for system health, cross-site tracking, and automated recovery.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    progress = st.progress(0)
    status = st.empty()

    for i in range(100):
        progress.progress(i + 1)
        if i < 30:
            message = "Starting core services..."
        elif i < 60:
            message = "Loading monitoring modules..."
        elif i < 90:
            message = "Syncing event and alert workflows..."
        else:
            message = "Finalizing dashboard state..."

        status.markdown(
            f"<div style='text-align:center; color:#64748b; margin-top:12px;'>" \
            f"<strong>{message}</strong> {i+1}%" \
            f"</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.02)

    st.success("Dashboard is ready. Navigate to Home or Error Monitor to begin.")
    time.sleep(0.8)
    st.session_state["loaded"] = True
    st.rerun()