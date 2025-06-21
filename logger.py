import os
from datetime import datetime

LOG_FILE = "logs/actions.log"

def log_action(action, filename, status, message =""):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action.upper()} | {filename.upper()} | {status.upper()} | {message}\n"

    with open(LOG_FILE, "a") as f:
        f.write(entry)



