import subprocess
import sys
import os
import webbrowser
import time

def main():
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    python_cmd = sys.executable if not getattr(sys, 'frozen', False) else "python"

    subprocess.Popen([
        python_cmd, "-m", "streamlit", "run", app_path,
        "--server.headless", "true",
        "--server.port", "8503"
    ])

    time.sleep(3) 
    webbrowser.open("http://localhost:8503")

if __name__ == "__main__":
    main()
