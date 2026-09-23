import json
import os

import config


def load():
    if not os.path.exists(config.STATE_FILE):
        return {"offset": None}
    with open(config.STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(state: dict):
    os.makedirs(os.path.dirname(config.STATE_FILE), exist_ok=True)
    with open(config.STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)
