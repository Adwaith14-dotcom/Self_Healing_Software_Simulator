import psutil

def capture_metrics():
    """Capture live system metrics"""
    return {
        "CPU": psutil.cpu_percent(interval=1),
        "Memory": psutil.virtual_memory().percent,
        "Disk": psutil.disk_usage('/').percent
    }