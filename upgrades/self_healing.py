import psutil
import streamlit as st
import os
from typing import List

def self_heal(cpu_threshold: int = 85,
              mem_threshold: int = 90,
              enable_healing: bool = True,
              show_banners: bool = True) -> None:
    """
    Self-healing logic that checks CPU and memory usage against thresholds
    and takes corrective actions if enabled. Also shows banners if requested.
    """

    if not enable_healing:
        return

    if "logs" not in st.session_state:
        st.session_state["logs"] = []

    logs: List[str] = st.session_state["logs"]

    cpu = psutil.cpu_percent(interval=1)
    if isinstance(cpu, (int, float)) and cpu > cpu_threshold:
        logs.append(f"[AUTO] High CPU ({cpu}%) detected 🔥 attempting to kill chrome.exe")
        if show_banners:
            st.error(f"⚠️ CPU usage high: {cpu}%")

        for proc in psutil.process_iter():
            try:
                if proc.name().lower() == "chrome.exe":
                    proc.kill()
                    logs.append("[AUTO] chrome.exe terminated successfully")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logs.append(f"[AUTO] Failed to kill chrome.exe: {e}")

    mem = psutil.virtual_memory().percent
    if isinstance(mem, (int, float)) and mem > mem_threshold:
        logs.append(f"[AUTO] High Memory ({mem}%) detected 🔥 running cleanmgr")
        if show_banners:
            st.warning(f"⚠️ Memory usage high: {mem}%")

        try:
            os.system("cleanmgr /sagerun:1")
            logs.append("[AUTO] Disk cleanup initiated")
        except Exception as e:
            logs.append(f"[AUTO] Cleanup failed: {e}")

    st.session_state["logs"] = logs

    for log in logs[-5:]:
        st.write(log)