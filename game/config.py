# config.py

import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent / "jsonconfigfiles/enemy.config.json"

with open(CONFIG_FILE) as f:
    CONFIG = json.load(f)


def get_config(key):
    return CONFIG.get(key)