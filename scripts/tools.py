import os
from datetime import datetime, timezone

def get_current_time() -> dict:
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"utc": current_time}

def get_all_files() -> dict:
    files = os.listdir('.')
    return {"files": files}