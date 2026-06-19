import pandas as pd
import streamlit as st

def add_error(category, error_type, message, severity="High"):
    """Log a new error into session state."""
    if "errors" not in st.session_state:
        st.session_state["errors"] = []
    st.session_state["errors"].append(
        {
            "Category": category,
            "Type": error_type,
            "Message": message,
            "Severity": severity,
            "Timestamp": pd.Timestamp.now()
        }
    )

def add_success(category, success_type, message):
    """Log a successful action into session state."""
    if "success" not in st.session_state:
        st.session_state["success"] = []
    st.session_state["success"].append(
        {
            "Category": category,
            "Type": success_type,
            "Message": message,
            "Timestamp": pd.Timestamp.now()
        }
    )

def resolve_error(index):
    """Move an error from Active Errors to Resolved Issues manually."""
    if "errors" in st.session_state and len(st.session_state["errors"]) > index:
        error = st.session_state["errors"].pop(index)
        error["ResolvedAt"] = pd.Timestamp.now()
        error["ResolutionMessage"] = "Manually resolved"
        if "resolved" not in st.session_state:
            st.session_state["resolved"] = []
        st.session_state["resolved"].append(error)

def auto_resolve(error_type, resolution_message="Auto-resolved after retry"):
    """
    Automatically resolve an error if conditions are met.
    Example: retry login/booking succeeds, mark error resolved.
    """
    if "errors" in st.session_state:
        for i, err in enumerate(st.session_state["errors"]):
            if err["Type"] == error_type:
                error = st.session_state["errors"].pop(i)
                error["ResolvedAt"] = pd.Timestamp.now()
                error["ResolutionMessage"] = resolution_message
                if "resolved" not in st.session_state:
                    st.session_state["resolved"] = []
                st.session_state["resolved"].append(error)
                break
