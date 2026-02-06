import time
from datetime import datetime
from colorama import init, Fore
import pyperclip
import keyboard

from app.config import load_config
from app.storage import load_history, save_history
from app.clipboard import paste_text
from app.pinning import compact_pin_order
from utils.helpers import compute_hash, calculate_score, parse_timestamp


class PaperClipZ:
    def __init__(self):
        init(autoreset=True)

        self.history_file = "data/history.json"
        self.config = load_config("data/config.json")

        self.interval = self.config.get("interval", 0.1)
        self.sort_mode = self.config.get("sort_mode", "smart")
        self.newline = self.config.get("newline", True)

        self.history = load_history(self.history_file)
        self.last_hash = ""
        self.is_pasting = False

        try:
            initial = pyperclip.paste()
            if initial:
                self.last_hash = compute_hash(initial)
        except Exception:
            pass

    def _sort_items(self, limit=10):
        pinned = [e for e in self.history if e.get("pinned")]
        unpinned = [e for e in self.history if not e.get("pinned")]

        pinned.sort(key=lambda e: e.get("pin_order", 0))

        if self.sort_mode == "last_copied":
            unpinned.sort(
                key=lambda e: parse_timestamp(
                    e.get("last_copied_at") or e.get("created_at")
                ),
                reverse=True,
            )
        else:
            unpinned.sort(key=calculate_score, reverse=True)

        return (pinned + unpinned)[:limit]
