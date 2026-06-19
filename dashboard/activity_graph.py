import streamlit as st
import psutil
import pandas as pd
import time

def show_activity_graph():
    cpu_data, mem_data = [], []
    for i in range(30):
        cpu_data.append(psutil.cpu_percent())
        mem_data.append(psutil.virtual_memory().percent)
        time.sleep(0.2)
    df_graph = pd.DataFrame({"CPU Usage": cpu_data, "Memory Usage": mem_data})
    st.line_chart(df_graph)