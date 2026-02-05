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
            interval: float = 0.1,
    ) -> None:
        init(autoreset=True)

        self.history_file = history_file
        self.config = self._load_config(config_file)

        self.interval = self.config.get("interval", interval)
        self.sort_mode = self.config.get("sort_mode", "smart")
        self.newline = self.config.get("newline", True)

        self.history: list[dict] = self._load_history()
        self.last_hash = ""
        self.is_pasting = False

        try:
            initial_text = pyperclip.paste()
            if initial_text:
                self.last_hash = self._compute_hash(initial_text)
        except Exception:
            pass

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

    def _save_history(self) -> None:
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"{Fore.RED}Error saving history: {e}")

    def _compute_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _find_entry(self, text_hash: str):
        for entry in self.history:
            if entry.get("id") == text_hash:
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

        last_pasted = entry.get("last_pasted_at")
        last_copied = entry.get("last_copied_at")
        created = entry.get("created_at")

        if last_pasted:
            timestamp = last_pasted
        elif last_copied:
            timestamp = last_copied
        else:
            timestamp = created

        dt = self._parse_timestamp(timestamp)

        if dt == datetime.min:
            return 0.0

        hours_ago = (now - dt).total_seconds() / 3600
        recency_score = math.exp(-hours_ago / 24)

        paste_count = entry.get("paste_count", 0)
        frequency_score = math.log(paste_count + 1)

        return (recency_score * 10) + (frequency_score * 2 * recency_score)

    def _sort_items(self, limit: int = 10) -> list[dict]:
        pinned = [e for e in self.history if e.get("pinned")]
        unpinned = [e for e in self.history if not e.get("pinned")]

        pinned.sort(key=lambda e: e.get("pin_order", 0))

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

    def _add_entry(self, text: str) -> None:
        text_hash = self._compute_hash(text)
        existing = self._find_entry(text_hash)

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

        self._save_history()

    def _paste_entry(self, index: int):
        items = self._sort_items(10)

        if index >= len(items):
            print(f"{Fore.RED}No item at position {index + 1}")
            return

        entry = items[index]
        original_text = entry["text"]

        text_to_paste = original_text
        if self.newline and not original_text.endswith(("\n", "\r\n")):
            text_to_paste += "\r\n"

        self.is_pasting = True
        self.last_hash = self._compute_hash(text_to_paste)

        pyperclip.copy(text_to_paste)
        keyboard.send("ctrl+v")

        entry["last_pasted_at"] = datetime.now().isoformat(timespec="seconds")
        entry["paste_count"] = entry.get("paste_count", 0) + 1

        self._save_history()

        display = original_text.strip()[:80]
        count = entry["paste_count"]
        pin_indicator = "📌 " if entry.get("pinned") else ""
        print(f"{Fore.BLUE}PASTED [{index + 1}]: {pin_indicator}pasted {count}x | {display}")

        time.sleep(0.05)
        self.is_pasting = False

    def _toggle_pin_current(self):
        try:
            current_text = pyperclip.paste()
        except:
            return

        if not current_text:
            return

        text_hash = self._compute_hash(current_text)
        entry = self._find_entry(text_hash)

        if not entry:
            print(f"{Fore.YELLOW}Item not in history")
            return

        if entry.get("pinned"):
            entry["pinned"] = False
            entry["pin_order"] = None

            self._compact_pin_order()

            display = current_text.strip()[:80]
            print(f"{Fore.YELLOW}UNPINNED: {display}")
        else:
            max_pin_order = max(
                (e.get("pin_order", -1) for e in self.history if e.get("pinned")),
                default=-1
            )
            entry["pinned"] = True
            entry["pin_order"] = max_pin_order + 1
            display = current_text.strip()[:80]
            print(f"{Fore.YELLOW}PINNED: {display}")

        self._save_history()

    def _compact_pin_order(self):
        pinned_items = [e for e in self.history if e.get("pinned")]
        pinned_items.sort(key=lambda e: e.get("pin_order", 0))

        for idx, entry in enumerate(pinned_items):
            entry["pin_order"] = idx

    def _hotkeys(self):
        for i in range(10):
            keyboard.add_hotkey(
                f"ctrl+{(i + 1) % 10}",
                lambda idx=i: self._paste_entry(idx),
                suppress=True,
            )

        keyboard.add_hotkey("ctrl+p", self._toggle_pin_current, suppress=True)

        print(f"{Fore.CYAN}Hotkeys: Ctrl+1-0 (paste), Ctrl+P (pin/unpin)")
        print(f"{Fore.CYAN}Sort mode: {self.sort_mode}")

    def run(self):
        print(f"{Fore.CYAN}PaperClipZ started (Ctrl+C to stop)")
        self._hotkeys()

        try:
            while True:
                try:
                    text = pyperclip.paste()
                except Exception:
                    time.sleep(self.interval)
                    continue

                if not text:
                    time.sleep(self.interval)
                    continue

                if self.is_pasting:
                    time.sleep(self.interval)
                    continue

                current_hash = self._compute_hash(text)
                if current_hash != self.last_hash:
                    self._add_entry(text)
                    self.last_hash = current_hash

                time.sleep(self.interval)
        except KeyboardInterrupt:
            print(f"{Fore.CYAN}\nPaperClipZ stopped")


if __name__ == "__main__":
    PaperClipZ().run()