import psutil
import platform
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import win32evtlog  

def log_event(message: str, details: str = ""):
    """Save events into Streamlit session logs."""
    if "logs" not in st.session_state:
        st.session_state["logs"] = []
    st.session_state["logs"].append(f"{message} {details}")

def check_resources(cpu_threshold: int = 85, mem_threshold: int = 90, disk_threshold: int = 95):
    cpu = cast(float, psutil.cpu_percent(interval=1, percpu=False))
    mem: float = psutil.virtual_memory().percent
    disk: float = psutil.disk_usage('/').percent

    if cpu > cpu_threshold:
        log_event("High CPU usage detected:", str(cpu))
    if mem > mem_threshold:
        log_event("High memory usage detected:", str(mem))
    if disk > disk_threshold:
        log_event("Disk usage critical:", str(disk))

    cpu_per_core = cast(list[float], psutil.cpu_percent(interval=1, percpu=True))
    for i, usage in enumerate(cpu_per_core):
        if usage > cpu_threshold:
            log_event(f"High CPU usage on core {i}:", str(usage))

def check_process(name: str) -> bool:
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        info = proc.as_dict(attrs=['pid', 'name'])
        if info.get('name') == name:
            return True
    return False

def monitor_processes():
    critical = ["explorer.exe", "python.exe"] 
    for proc in critical:
        if not check_process(proc):
            log_event("Critical process stopped:", proc)

def monitor_system_logs():
    if platform.system() == "Windows":
        try:
            import win32evtlog 
            server = 'localhost'
            log_type = 'System'
            hand = win32evtlog.OpenEventLog(server, log_type)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            for e in events:
                if "Error" in str(e):
                    log_event("System error detected:", str(e))
        except ImportError:
            log_event("Windows Event Log not available", "")
    else:
        try:
            with open("/var/log/syslog", "r") as f:
                for line in f.readlines()[-50:]:
                    if "error" in line.lower():
                        log_event("System error detected:", line.strip())
        except Exception as e:
            log_event("Error reading syslog:", str(e))

if "metric_history" not in st.session_state:
    st.session_state.metric_history = pd.DataFrame(columns=["Time", "CPU", "Memory", "Disk"])

def gauge_chart(value, title, color):
    """Speedometer-style semicircle gauge."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 14}},
        number={'font': {'size': 16, 'color': color}, 'valueformat': '.1f'},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'shape': "angular",
            'steps': [
                {'range': [0, 50], 'color': "lightgreen"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "red"}
            ],
        },
        domain={'x': [0, 1], 'y': [0, 0.7]}
    ))
    fig.update_layout(height=180, margin=dict(t=0, b=0, l=0, r=0))
    return fig

def show_monitoring_section():
    """Monitoring window with gauges + trends."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    new_row = {"Time": pd.Timestamp.now(), "CPU": cpu, "Memory": mem, "Disk": disk}
    st.session_state.metric_history = pd.concat(
        [st.session_state.metric_history, pd.DataFrame([new_row])],
        ignore_index=True
    ).tail(100)

    st.markdown("### 🧠 System Health")
    col1, col2, col3 = st.columns(3)
    with col1: st.plotly_chart(gauge_chart(cpu, "CPU Usage", "blue"), use_container_width=True)
    with col2: st.plotly_chart(gauge_chart(mem, "Memory Usage", "purple"), use_container_width=True)
    with col3: st.plotly_chart(gauge_chart(disk, "Disk Usage", "orange"), use_container_width=True)

    st.markdown("### 📈 Performance Trends")
    df = st.session_state.metric_history.tail(30)
    fig = px.line(
        df, x="Time", y=["CPU", "Memory", "Disk"],
        labels={"value": "Usage %", "variable": "Metric"},
        title="System Usage Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)