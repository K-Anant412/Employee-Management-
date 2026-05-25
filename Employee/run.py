import subprocess
import time
import sys

backend = subprocess.Popen(
    [sys.executable, "app.py"]
)

time.sleep(2)

frontend = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app_ui.py"]
)

backend.wait()
frontend.wait()