import streamlit as st
from debugger.viewer import show_debugger # type: ignore
from debugger.escalation import escalate_errors
from upgrades.error_handler import detect_errors, analyze_error, heal_error, log_error

def run_debugger():
    st.header("🪲 Debugger Window")

    errors = detect_errors()
    if not errors:
        st.success("✅ No errors detected.")
        return

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

    show_debugger(logs)

if __name__ == "__main__":
    run_debugger()