import psutil
import logging
import socket

logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def detect_errors():
    errors = []

    for proc in psutil.process_iter():
        try:
            pid = proc.pid
            name = proc.name()
            status = proc.status()
            mem = proc.memory_info().rss

            if status == psutil.STATUS_ZOMBIE:
                errors.append((pid, name, "Zombie process"))
            elif mem > 500 * 1024 * 1024:
                errors.append((pid, name, f"High memory usage: {mem / (1024*1024):.1f} MB"))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        except Exception as e:
            errors.append(("Unknown", "Process check failed", str(e)))

    try:
        disk = psutil.disk_usage('/')
        if disk.percent > 90:
            errors.append(("Disk", "Root Partition", f"High disk usage: {disk.percent}%"))
    except Exception as e:
        errors.append(("Disk", "Check failed", str(e)))

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except Exception as e:
        errors.append(("Network", "Connectivity", f"Network error: {str(e)}"))

    return errors

def analyze_error(error):
    pid, name, message = error
    msg_lower = message.lower()
    if "zombie" in msg_lower:
        return f"Process {name} (PID {pid}) crashed without cleanup."
    elif "memory" in msg_lower:
        return f"Process {name} (PID {pid}) is consuming too much memory."
    elif "disk" in msg_lower:
        return f"Disk space critically low on {name}."
    elif "network" in msg_lower:
        return f"Network connectivity issue detected."
    else:
        return f"Error in {name}: {message}"

def heal_error(error):
    pid, name, message = error
    msg_lower = message.lower()
    try:
        if "zombie" in msg_lower or "memory" in msg_lower:
            psutil.Process(pid).kill()
            return f"Killed problematic process {name} (PID {pid})."
        elif "disk" in msg_lower:
            return "Suggested fix: clear temporary files or expand disk capacity."
        elif "network" in msg_lower:
            return "Suggested fix: check internet connection or restart network service."
        else:
            return f"No automatic fix available for {name}."
    except Exception as e:
        return f"Healing failed: {str(e)}"

def log_error(error, analysis, solution):
    logging.error(f"Error: {error} | Root Cause: {analysis} | Solution: {solution}")