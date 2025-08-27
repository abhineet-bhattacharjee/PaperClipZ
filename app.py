import pyperclip
import keyboard

import os
import time
import json
from datetime import datetime


class PaperClipZ:
    def __init__(self, history_file: str = 'history.json', interval: float = 1.0) -> None:
        self.history_file: str = history_file
        self.interval: float = interval
        self.history: list[dict] = self._load_history()

    def _load_history(self) -> list[dict]:
        if not os.path.exists(self.history_file):
            return []
        with open(self.history_file, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _save_history(self) -> None:
        with open(self.history_file, '', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def _add_entry(self, text) -> None:
        entry = {
            'text': text,
            'timestamp': datetime.now().isoformat(timespec='seconds')
        }
        self.history.append(entry)
        self._save_history()
        print(f'✔ Saved: {text[:40]}{"..." if len(text) > 40 else ""}')

    def run(self):
        pass
