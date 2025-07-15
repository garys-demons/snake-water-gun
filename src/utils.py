import json
import csv
import os
from datetime import datetime
from src.constants import SCORE_FILE, HISTORY_FILE

def load_top_score():
    if not os.path.exists(SCORE_FILE):
        return 0
    try:
        with open(SCORE_FILE, "r") as f:
            data = f.read().strip()
            return json.loads(data).get("top_score", 0) if data else 0
    except Exception:
        return 0

def save_top_score(score):
    try:
        os.makedirs(os.path.dirname(SCORE_FILE), exist_ok=True)
        with open(SCORE_FILE, "w") as f:
            json.dump({"top_score": score}, f)
    except Exception:
        pass

def append_history(player, computer, result):
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), player, computer, result])
    except Exception:
        pass
