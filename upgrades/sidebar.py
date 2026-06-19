import streamlit as st

def show_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #1e1e2f;
            color: white;
        }
        div[data-testid="stSidebarNav"] > div {
            padding-top: 20px;
        }
        div[role="radiogroup"] > label[data-baseweb="radio"] {
            background-color: transparent;
            padding: 8px 16px;
            border-radius: 6px;
            margin-bottom: 4px;
            font-weight: 500;
        }
        div[role="radiogroup"] > label[data-baseweb="radio"]:hover {
            background-color: #2c3e50;
        }
        div[role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"] {
            background-color: #007acc;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("Self-Healing Software Simulator")

    section = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "📊 Monitoring Window",
            "⚙️ Settings",
            "📜 Logs",
            "🪲 Debugger",
            "🛡️ Tools",
            "🛠️ Error Monitor"
        ]
    )

    return section
