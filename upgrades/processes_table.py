import streamlit as st
import psutil
import pandas as pd

def show_processes_table():
    procs = []
    for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent']):
        procs.append(p.as_dict(attrs=['pid','name','cpu_percent','memory_percent']))
    df = pd.DataFrame(procs).sort_values("cpu_percent", ascending=False).head(10)

    st.subheader("⚙️ Top Processes")
    st.dataframe(df[['pid','name','cpu_percent','memory_percent']], use_container_width=True)