import pyperclip
import keyboard
import os
import time
import json
import hashlib
import math
from datetime import datetime
from colorama import init, Fore


class PaperClipZ:
    def __init__(
        self,
        history_file: str = "history.json",
        config_file: str = "config.json",
        interval: float = 1.0,
    ) -> None:
        init(autoreset=True)

        self.history_file = history_file
        self.config = self._load_config(config_file)

        self.interval = self.config.get("interval", interval)
        self.sort_mode = self.config.get("sort_mode", "last_copied")
        self.newline = self.config.get("newline", True)

        # Load history FIRST
        self.history: list[dict] = self._load_history()

        # Normalize pin order ONCE
        self._normalize_pins()

        try:
            self.last_text = pyperclip.paste()
        except Exception:
            self.last_text = ""

    # ---------- CONFIG / STORAGE ----------

    def _load_config(self, path: str) -> dict:
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _load_history(self) -> list[dict]:
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_history(self) -> None:
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    # ---------- PIN LOGIC (SINGLE SOURCE OF TRUTH) ----------

    def _normalize_pins(self) -> None:
        pinned = [e for e in self.history if e.get("pinned")]
        pinned.sort(key=lambda e: e.get("pin_order", float("inf")))

        for idx, entry in enumerate(pinned):
            entry["pin_order"] = idx

    # ---------- UTILS ----------

    def _compute_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _find_entry(self, text_hash: str):
        for entry in self.history:
            if entry["id"] == text_hash:
                return entry
        return None

    def _parse_timestamp(self, ts: str | None):
        if not ts:
            return datetime.min
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            return datetime.min

    def _calculate_score(self, entry: dict) -> float:
        now = datetime.now()
        last = (
            entry.get("last_pasted_at")
            or entry.get("last_copied_at")
            or entry.get("created_at")
        )

        dt = self._parse_timestamp(last)
        hours_ago = (now - dt).total_seconds() / 3600 if dt != datetime.min else 9999
        recency = math.exp(-hours_ago / 24)

        freq = math.log(entry.get("paste_count", 0) + 1)
        return recency * 10 + freq * 2 * recency

    # ---------- SORTING ----------

    def _sort_items(self, limit: int = 10) -> list[dict]:
        pinned = [e for e in self.history if e.get("pinned")]
        unpinned = [e for e in self.history if not e.get("pinned")]

        pinned.sort(key=lambda e: e["pin_order"])

        if self.sort_mode == "last_copied":
            unpinned.sort(
                key=lambda e: self._parse_timestamp(
                    e.get("last_copied_at") or e.get("created_at")
                ),
                reverse=True,
            )
        else:
            unpinned.sort(key=self._calculate_score, reverse=True)

        return (pinned + unpinned)[:limit]

    # ---------- CORE FEATURES ----------

    def _add_entry(self, text: str) -> None:
        text_hash = self._compute_hash(text)
        existing = self._find_entry(text_hash)

        if existing:
            existing["last_copied_at"] = datetime.now().isoformat(timespec="seconds")
            existing["copy_count"] = existing.get("copy_count", 0) + 1
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

        self._save_history()

    def _paste_entry(self, index: int):
        items = self._sort_items(10)
        if index >= len(items):
            return

        entry = items[index]
        text = entry["text"]

        if self.newline and not text.endswith(("\n", "\r\n")):
            text += "\r\n"

        pyperclip.copy(text)
        keyboard.send("ctrl+v")

        entry["last_pasted_at"] = datetime.now().isoformat(timespec="seconds")
        entry["paste_count"] = entry.get("paste_count", 0) + 1

        self._save_history()

        print(f"{Fore.BLUE}PASTED [{index + 1}]")

    # ---------- HOTKEYS ----------

    def _hotkeys(self):
        for i in range(10):
            keyboard.add_hotkey(
                f"ctrl+{(i + 1) % 10}",
                lambda idx=i: self._paste_entry(idx),
                suppress=True,
            )

        print(f"{Fore.CYAN}Ctrl+1 → Ctrl+0 bound")

    # ---------- LOOP ----------

    def run(self):
        print(f"{Fore.CYAN}Clipboard logger started")
        self._hotkeys()

        try:
            while True:
                try:
                    text = pyperclip.paste()
                except Exception:
                    time.sleep(self.interval)
                    continue

                if text and text != self.last_text:
                    self._add_entry(text)
                    self.last_text = text

                time.sleep(self.interval)
        except KeyboardInterrupt:
            print(f"{Fore.CYAN}\nStopped")


if __name__ == "__main__":
    PaperClipZ().run()
