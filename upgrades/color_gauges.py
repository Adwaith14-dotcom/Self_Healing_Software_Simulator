import psutil
import streamlit as st

def show_color_gauges(metric: str = "CPU"):
    """
    Display a gauge for either CPU or Memory usage.
    """
    if metric == "CPU":
        value = psutil.cpu_percent(interval=1)
        st.metric(label="CPU Usage", value=f"{value} %")
    elif metric == "Memory":
        value = psutil.virtual_memory().percent
        st.metric(label="Memory Usage", value=f"{value} %")
    else:
        st.warning("Unknown metric type")