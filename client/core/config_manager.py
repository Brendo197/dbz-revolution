import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "resolution": 2,
    "save_password": False,
    "username": "",
    "password": ""
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # garante que chaves padrão existam
        for key, value in DEFAULT_CONFIG.items():
            if key not in data:
                data[key] = value

        return data

    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(data: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass