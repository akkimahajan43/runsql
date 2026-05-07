import os
import sys
import threading
import time
import webbrowser
from streamlit.web import cli as stcli

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_PATH = os.path.join(BASE_DIR, "app.py")

def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":

    threading.Thread(target=open_browser).start()

    sys.argv = [
        "streamlit",
        "run",
        APP_PATH,
        "--server.headless=true"
    ]

    sys.exit(stcli.main())