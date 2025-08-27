import pyperclip
import keyboard

import os
import time
import json
from datetime import datetime

class PaperClipZ:
    def __init__(self, history_file: str='history.json', interval: float=1.0) -> None:
        self.history_file: str = history_file
        self.interval: float = interval


    def _load_history(self) -> list[dict]:
        with open(self.history_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_history(self):
        pass

    def _add_entry(self, text):
        pass

    def run(self):
        pass