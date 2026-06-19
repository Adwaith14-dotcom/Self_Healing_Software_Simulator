import streamlit as st
import psutil
from debugger.metrics import capture_metrics

def show_top_processes():
    processes = []
    for proc in psutil.process_iter():
        try:
            processes.append((proc.pid, proc.name(), proc.memory_info().rss))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    processes = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
    return [{"PID": p[0], "Name": p[1], "Memory MB": round(p[2]/1024/1024, 1)} for p in processes]

def show_alerts(metrics):
    alerts = []
    if metrics["Memory"] > 70:
        alerts.append(f"⚠️ High Memory usage: {metrics['Memory']}%")
    if metrics["Disk"] > 65:
        alerts.append(f"⚠️ Disk almost full: {metrics['Disk']}%")
    return alerts

def show_debugger_section(errors):
   
    metrics = capture_metrics()

    st.markdown("### 🚨 System Alerts")
    alerts = show_alerts(metrics)
    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("✅ No critical alerts.")

    st.markdown("### ⚙️ Top Processes")
    st.table(show_top_processes())
   
    st.markdown("### 📝 Error Logs & Severity")
    if errors:
        for err in errors:
            msg = str(err)
            if "Zombie" in msg or "High memory" in msg:
                st.error(msg)
            elif "disk" in msg.lower() or "network" in msg.lower():
                st.warning(msg)
            else:
                st.info(msg)
    else:
        st.success("✅ No errors detected.")