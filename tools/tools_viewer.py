import streamlit as st
import psutil
import pandas as pd
import random
from io import BytesIO

def show_tools_section():
    col1, col2, col3 = st.columns(3)

    # --- Disk Health ---
    with col1:
        st.markdown("### 💽 Disk Health")
        disk = psutil.disk_usage('/')
        usage = disk.percent
        free_gb = round(disk.free / (1024**3), 1)
        total_gb = round(disk.total / (1024**3), 1)
        temp = random.randint(30, 45)

        st.metric("Usage", f"{usage}%")
        if usage < 70:
            st.success("Status: Good")
        elif usage < 90:
            st.warning("Status: Moderate")
        else:
            st.error("Status: Critical")

        st.caption(f"Free Space: {free_gb} GB / {total_gb} GB")
        st.caption(f"Temperature: {temp}°C")

    # --- Data Export ---
    with col2:
        st.markdown("### 📤 Data Export")

        # Example logs DataFrame (replace with your actual logs)
        logs_df = pd.DataFrame({
            "Error": ["High CPU usage", "High Memory usage"],
            "Severity": ["Warning", "Critical"]
        })

        metrics_df = st.session_state.get("metric_history", pd.DataFrame())

        # Export Logs
        csv_logs = logs_df.to_csv(index=False).encode("utf-8")
        st.download_button("📑 Export Logs (CSV)", csv_logs, "logs.csv", "text/csv", use_container_width=True)

        buffer_logs = BytesIO()
        with pd.ExcelWriter(buffer_logs, engine="openpyxl") as writer:
            logs_df.to_excel(writer, index=False, sheet_name="Logs")
        st.download_button("📑 Export Logs (Excel)", buffer_logs.getvalue(),
                           "logs.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

        # Export Metrics
        if not metrics_df.empty:
            csv_metrics = metrics_df.to_csv(index=False).encode("utf-8")
            st.download_button("📊 Download Metrics (CSV)", csv_metrics, "metrics.csv", "text/csv", use_container_width=True)

            buffer_metrics = BytesIO()
            with pd.ExcelWriter(buffer_metrics, engine="openpyxl") as writer:
                metrics_df.to_excel(writer, index=False, sheet_name="Metrics")
            st.download_button("📊 Download Metrics (Excel)", buffer_metrics.getvalue(),
                               "metrics.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        else:
            st.info("ℹ️ No metrics available to export.")

        # Generate Report (Logs + Metrics)
        if not metrics_df.empty:
            report_df = pd.concat([logs_df, metrics_df], axis=1)
        else:
            report_df = logs_df

        csv_report = report_df.to_csv(index=False).encode("utf-8")
        st.download_button("📈 Generate Report (CSV)", csv_report, "report.csv", "text/csv", use_container_width=True)

        buffer_report = BytesIO()
        with pd.ExcelWriter(buffer_report, engine="openpyxl") as writer:
            logs_df.to_excel(writer, index=False, sheet_name="Logs")
            if not metrics_df.empty:
                metrics_df.to_excel(writer, index=False, sheet_name="Metrics")
        st.download_button("📈 Generate Report (Excel)", buffer_report.getvalue(),
                           "report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

        st.caption("Format Options")
        st.radio("Format", ["CSV", "Excel", "JSON"], index=0, horizontal=True)
        st.caption("Retention Period")
        st.slider("Days", 7, 30, 15)

    # --- Process Manager ---
    with col3:
        st.markdown("### ⚙️ Process Manager")
        processes = []
        for proc in psutil.process_iter():
            try:
                name = proc.name() or "Unknown"
                mem = proc.memory_info().rss // (1024**2)
                processes.append((proc.pid, name, mem))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        df = pd.DataFrame(processes, columns=["PID", "Name", "Memory MB"])
        st.dataframe(df.head(5), use_container_width=True)

        pid_to_kill = st.number_input("Enter PID to terminate", min_value=0, step=1)
        if st.button("End Selected", type="primary", use_container_width=True):
            if pid_to_kill > 0:
                try:
                    proc = psutil.Process(pid_to_kill)
                    proc.terminate()
                    st.success(f"✅ Process {pid_to_kill} terminated.")
                except Exception as e:
                    st.error(f"⚠️ Could not terminate process {pid_to_kill}: {e}")
            else:
                st.warning("Please enter a valid PID.")

        if st.button("Refresh List", use_container_width=True):
            df = pd.DataFrame(processes, columns=["PID", "Name", "Memory MB"])
            st.dataframe(df.head(5), use_container_width=True)