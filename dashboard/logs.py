import streamlit as st

def show_logs():
    log_messages = [
        "[20:15:32] System check completed successfully.",
        "[20:16:01] High CPU usage detected.",
        "[20:16:25] Restarted Apache service.",
        "[20:17:10] Memory usage at 85% - Warning.",
        "[20:18:45] Disk cleanup initiated.",
        "[20:19:30] Error: Unable to connect to database!"
    ]
    with st.expander("📜 Event Logs"):
        for msg in log_messages:
            if "Error" in msg:
                st.error(msg)
            elif "Warning" in msg:
                st.warning(msg)
            elif "successful" in msg:
                st.success(msg)
            else:
                st.info(msg)