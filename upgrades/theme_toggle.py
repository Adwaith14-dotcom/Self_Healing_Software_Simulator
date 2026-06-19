import streamlit as st

def theme_toggle(key: str = "theme_toggle"):
    theme = st.radio("Theme", ["Light", "Dark"], key=key)
    if theme == "Dark":
        st.markdown("<style>body { background-color: #111; color: white; }</style>", unsafe_allow_html=True)
    else:
        st.markdown("<style>body { background-color: white; color: black; }</style>", unsafe_allow_html=True)