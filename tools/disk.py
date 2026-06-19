import streamlit as st
import psutil
import plotly.graph_objects as go

def disk_usage_gauge():
    """Show disk usage as a semicircle gauge."""
    usage = psutil.disk_usage('/').percent
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=usage,
        title={'text': "Disk Usage", 'font': {'size': 14}},
        number={'font': {'size': 16, 'color': "orange"}, 'valueformat': '.1f'},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "orange"},
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
    st.plotly_chart(fig, use_container_width=True)

def run_disk_check():
    """Disk tool section with gauge + details."""
    st.subheader("💽 Disk Health Tool")

    disk_usage_gauge()

    usage = psutil.disk_usage('/')
    st.write(f"**Total:** {usage.total / (1024**3):.1f} GB")
    st.write(f"**Used:** {usage.used / (1024**3):.1f} GB")
    st.write(f"**Free:** {usage.free / (1024**3):.1f} GB")
    st.write(f"**Usage:** {usage.percent}%")

    if st.button("Run Disk Check"):
        if usage.percent > 90:
            st.error("⚠️ Disk usage critical! Consider freeing space.")
        elif usage.percent > 70:
            st.warning("⚠️ Disk usage high. Monitor closely.")
        else:
            st.success("✅ Disk usage is healthy.")