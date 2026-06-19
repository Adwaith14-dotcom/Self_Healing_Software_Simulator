import streamlit as st
from debugger.escalation import escalate_errors
from upgrades.error_handler import detect_errors, analyze_error, heal_error, log_error

def show_event_logs():
    st.header("📜 Event Logs")

    errors = detect_errors()
    if not errors:
        st.success("✅ No errors detected.")
        return []

    data = []
    for idx, error in enumerate(errors, start=1):
        analysis = analyze_error(error)
        solution = heal_error(error)
        log_error(error, analysis, solution)
        data.append({
            "Serial": idx,
            "Error": str(error),
            "Root Cause": analysis,
            "Solution": solution
        })

    logs = escalate_errors(data)

    st.write("Here are the detected errors:")
    st.dataframe(logs, use_container_width=True)

    return logs