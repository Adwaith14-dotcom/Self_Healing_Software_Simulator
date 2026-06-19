import streamlit as st
from web_monitor.demo_site import generate_demo_error, save_demo_event

st.set_page_config(page_title="Demo Event Generator", layout="centered")

st.title("Demo Event Generator")

st.markdown(
    "Use this app to create clean, structured event payloads for the self-healing simulator. "
    "The simulator consumes both live service events and generated demo events so you can verify cross-site detection and recovery."
)

site_choice = st.selectbox(
    "Target site or service",
    ["Authentication Service", "Booking Service", "Cache Manager", "System Monitor", "Background Service"]
)

error_choice = st.selectbox(
    "Error scenario",
    ["LoginError", "ServiceCrash", "HighCPU", "MinorWarning", "InfoEvent"]
)

if st.button("Trigger Event"):
    event = generate_demo_error(error_choice)
    event["Site"] = site_choice
    save_demo_event(event)
    st.success(f"Event created for {site_choice} with type {event['Type']}")
    st.write("The simulator will automatically load this event the next time it checks for incoming signals.")

st.divider()

st.markdown(
    "### Notes"
    "\n- This generator creates events that the main simulator can process alongside live monitoring feeds."
    "\n- Keep this app open while the self-healing dashboard is running to validate detection and alert behavior."
)
