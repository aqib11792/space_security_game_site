import json

PROGRESS_FILE = "data/progress.json"

def load_progress(username):
    try:
        with open(PROGRESS_FILE) as f:
            return json.load(f).get(username, {"score": 0, "level": 1})
    except:
        return {"score": 0, "level": 1}

def save_progress(username, data):
    try:
        with open(PROGRESS_FILE) as f:
            all_data = json.load(f)
    except:
        all_data = {}
    all_data[username] = data
    with open(PROGRESS_FILE, "w") as f:
        json.dump(all_data, f, indent=2)