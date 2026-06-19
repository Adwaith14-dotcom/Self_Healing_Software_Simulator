import streamlit as st
import psutil

def show_summary_panel():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    battery = psutil.sensors_battery()

    st.subheader("📊 System Summary")
    st.write(f"CPU Load: {cpu}% | Memory: {mem.percent}% | Battery: {battery.percent if battery else 'N/A'}%")