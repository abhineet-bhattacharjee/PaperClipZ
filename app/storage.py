import os
import json
from datetime import datetime
from colorama import Fore


class Storage:
    def __init__(self, history_file: str = "data/history.json"):
        self.history_file = history_file
        self.history: list[dict] = self._load()

    def _load(self) -> list[dict]:
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
                for entry in history:
                    if "last_pasted_at" not in entry:
                        entry["last_pasted_at"] = None
                    if "paste_count" not in entry:
                        entry["paste_count"] = 0
                    if "last_copied_at" not in entry:
                        entry["last_copied_at"] = entry.get("created_at")
                    if "copy_count" not in entry:
                        entry["copy_count"] = 1
                    if "pinned" not in entry:
                        entry["pinned"] = False
                    if "pin_order" not in entry:
                        entry["pin_order"] = None
                return history
        except Exception:
            return []

    def save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"{Fore.RED}Error saving history: {e}")

    def find_entry(self, text_hash: str):
        for entry in self.history:
            if entry.get("id") == text_hash:
                return entry
        return None

    def add_entry(self, text: str, text_hash: str) -> None:
        existing = self.find_entry(text_hash)

        if existing:
            existing["last_copied_at"] = datetime.now().isoformat(timespec="seconds")
            existing["copy_count"] = existing.get("copy_count", 0) + 1

            display = text.strip()[:80]
            count = existing["copy_count"]
            pin_indicator = "📌 " if existing.get("pinned") else ""
            print(f"{Fore.LIGHTGREEN_EX}UPDATE: {pin_indicator}copied {count}x | {display}")
        else:
            entry = {
                "id": text_hash,
                "text": text,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "last_copied_at": datetime.now().isoformat(timespec="seconds"),
                "last_pasted_at": None,
                "copy_count": 1,
                "paste_count": 0,
                "pinned": False,
                "pin_order": None,
            }
            self.history.append(entry)

            display = text.strip()[:80]
            print(f"{Fore.GREEN}SAVED: {display}")

        self.save()

    def update_paste_stats(self, entry: dict) -> None:
        entry["last_pasted_at"] = datetime.now().isoformat(timespec="seconds")
        entry["paste_count"] = entry.get("paste_count", 0) + 1
        self.save()
