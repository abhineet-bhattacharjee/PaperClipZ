import json
import os
from datetime import datetime


def load_history(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            history = json.load(f)

        for entry in history:
            entry.setdefault("last_pasted_at", None)
            entry.setdefault("paste_count", 0)
            entry.setdefault("last_copied_at", entry.get("created_at"))
            entry.setdefault("copy_count", 1)
            entry.setdefault("pinned", False)
            entry.setdefault("pin_order", None)

        return history
    except Exception:
        return []


def save_history(path: str, history: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)