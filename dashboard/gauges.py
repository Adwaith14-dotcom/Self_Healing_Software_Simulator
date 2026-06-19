import streamlit as st
import psutil

def show_gauges():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    battery = psutil.sensors_battery()

    col1, col2, col3 = st.columns(3)
    col1.metric("💻 CPU Usage", f"{cpu}%")
    col2.metric("🧠 Memory Usage", f"{mem.percent}%")
    col3.metric("🔋 Battery", f"{battery.percent if battery else 0}%")