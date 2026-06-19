import streamlit as st
import psutil
import pandas as pd

def get_top_processes(limit=10):
    """Return top processes by memory usage."""
    processes = []
    for proc in psutil.process_iter():
        try:
            pid = proc.pid
            name = proc.name()
            mem = proc.memory_info().rss
            cpu = proc.cpu_percent(interval=0.1)
            processes.append({
                "PID": pid,
                "Name": name,
                "Memory MB": round(mem / 1024 / 1024, 1),
                "CPU %": cpu
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    df = pd.DataFrame(processes)
    df = df.sort_values(by="Memory MB", ascending=False).head(limit)
    return df

def show_process_manager():
    """Process Manager tool with table + actions."""
    st.subheader("⚙️ Process Manager")

    df = get_top_processes()
    st.dataframe(df, use_container_width=True)

    # Select process by PID
    pid_to_kill = st.number_input("Enter PID to terminate", min_value=0, step=1)

    if st.button("Terminate Process"):
        if pid_to_kill > 0:
            try:
                proc = psutil.Process(pid_to_kill)
                proc.terminate()
                st.success(f"✅ Process {pid_to_kill} terminated.")
            except Exception as e:
                st.error(f"⚠️ Could not terminate process {pid_to_kill}: {e}")
        else:
            st.warning("Please enter a valid PID.")

    # Refresh button
    if st.button("🔄 Refresh Process List"):
        df = get_top_processes()
        st.dataframe(df, use_container_width=True)

    # Extra: Kill top memory process quickly
    if st.button("⚡ End Top Memory Process"):
        if not df.empty:
            top_pid = df.iloc[0]["PID"]
            try:
                proc = psutil.Process(top_pid)
                proc.terminate()
                st.success(f"✅ Top memory process {top_pid} terminated.")
            except Exception as e:
                st.error(f"⚠️ Could not terminate process {top_pid}: {e}")