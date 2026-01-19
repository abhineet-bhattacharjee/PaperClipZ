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
        try:
            self.last_text: str = pyperclip.paste()
        except:
            self.last_text: str = ''

    def _load_history(self) -> list[dict]:
        if not os.path.exists(self.history_file):
            return []
        with open(self.history_file, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _save_history(self) -> None:
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f'❌ Error saving history: {e}')

    def _add_entry(self, text: str) -> None:
        entry = {
            'text': text,
            'timestamp': datetime.now().isoformat(timespec='seconds')
        }
        self.history.append(entry)
        self._save_history()
        print(f'✔ Saved: {text[:100]}{"..." if len(text) > 100 else ""}\n')

    def _paste_entry(self, index: int):
        if not self.history:
            print("⚠ No history to paste from.")
            return

        recent_history = self.history[-10:][::-1]

        if index >= len(recent_history):
            print(f"⚠ Invalid index for pasting. Only {len(recent_history)} items available.")
            return

        text_to_paste = recent_history[index]['text']
        pyperclip.copy(text_to_paste)
        keyboard.send('ctrl+v')

        print(f'📋 Pasted [{index}]: {text_to_paste[:100]}{"..." if len(text_to_paste) > 100 else ""}')

    def _hotkeys(self):
        for i in range(1, 10):
            keyboard.add_hotkey(f'ctrl+{i}', lambda idx=i - 1: self._paste_entry(idx))

        keyboard.add_hotkey('ctrl+0', lambda idx=9: self._paste_entry(idx))

        print('⌨ Hotkeys registered:')
        print('  Ctrl+1 = Most recent')
        print('  Ctrl+2 = 2nd most recent')
        print('  ...')
        print('  Ctrl+0 = 10th most recent\n')

    def run(self) -> None:
        print('📋 Clipboard logger started... (Ctrl+C to trigger)')
        self._hotkeys()

        try:
            while True:
                try:
                    text: str = pyperclip.paste()
                except:
                    print('⚠ Clipboard access failed, retrying...')
                    time.sleep(self.interval)
                    continue

                if text and text != self.last_text:
                    self._add_entry(text)
                    self.last_text = text
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print('\n🛑 Clipboard logger stopped.')


if __name__ == '__main__':
    app = PaperClipZ()
    app.run()