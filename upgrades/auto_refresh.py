import streamlit as st

def enable_auto_refresh(interval: int = 5):
    """
    Manual refresh + optional auto-refresh toggle.
    """
    if st.button("🔄 Refresh Now"):
        st.rerun()

    auto = st.checkbox("Enable auto-refresh")
    if auto:
        st.toast(f"Auto-refresh every {interval} seconds enabled")
        st.session_state["refresh_interval"] = interval