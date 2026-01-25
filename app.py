import pyperclip
import keyboard

import os
import time
import json
import hashlib
from datetime import datetime


class PaperClipZ:
    def __init__(self, history_file: str = 'history.json', interval: float = 1.0) -> None:
        self.history_file: str = history_file
        self.interval: float = interval
        self.history: list[dict] = self._load_history()
        self.newline = True
        try:
            self.last_text: str = pyperclip.paste()
        except:
            self.last_text: str = ''

    def _compute_hash(self, text: str):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def _find_entry_by_hash(self, text_hash: str):
        for entry in self.history:
            if entry.get('id') == text_hash:
                return entry
        return None

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
            print(f'Error saving history: {e}')

    def _add_entry(self, text: str) -> None:
        text_hash = self._compute_hash(text)
        existing_entry = self._find_entry_by_hash(text_hash)

        if existing_entry:
            self.history.remove(existing_entry)
            existing_entry['last_used'] = datetime.now().isoformat(timespec='seconds')
            existing_entry['copy_count'] += 1
            self.history.append(existing_entry)
            print(f'UPDATE LOG: (copied {existing_entry["copy_count"]} times(s)): {text.strip()[:100]}{"..." if len(text) > 100 else ""}')
        else:
            entry = {
                'id': text_hash,
                'text': text,
                'created_at': datetime.now().isoformat(timespec='seconds'),
                'last_used': datetime.now().isoformat(timespec='seconds'),
                'copy_count': 1
            }
            self.history.append(entry)
            print(f'SAVE LOG {len(self.history)}: {text.strip()[:100]}{"..." if len(text) > 100 else ""}')

        self._save_history()

    def _paste_entry(self, index: int):
        if not self.history:
            print("No history to paste from.")
            return

        recent_history = self.history[-10:][::-1]

        if index >= len(recent_history):
            print(f"Invalid index for pasting. Only {len(recent_history)} items available.")
            return

        text_to_paste = recent_history[index]['text']
        text_to_paste += '\r\n' if not text_to_paste.endswith(('\n', '\r\n')) and self.newline else ''
        pyperclip.copy(text_to_paste)

        self.last_text = text_to_paste
        keyboard.send('ctrl+v')

        print(f'PASTED [{index}]: {text_to_paste.strip()[:100]}{"..." if len(text_to_paste) > 100 else ""}')

    def _hotkeys(self):
        for i in range(1, 10):
            keyboard.add_hotkey(f'ctrl+{i}', lambda idx=i - 1: self._paste_entry(idx), suppress=True)

        keyboard.add_hotkey('ctrl+0', lambda idx=9: self._paste_entry(idx), suppress=True)

        print('Hotkeys registered:')
        print('  Ctrl+1 = Most recent')
        print('  Ctrl+2 = 2nd most recent')
        print('  ...')
        print('  Ctrl+0 = 10th most recent\n')

    def run(self) -> None:
        print('Clipboard logger started... (Ctrl+C to trigger)')
        self._hotkeys()

        try:
            while True:
                try:
                    text: str = pyperclip.paste()
                except:
                    print('Clipboard access failed, retrying...')
                    time.sleep(self.interval)
                    continue

                if text and text != self.last_text:
                    self._add_entry(text)
                    self.last_text = text
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print('\nClipboard logger stopped.')


if __name__ == '__main__':
    app = PaperClipZ()
    app.run()
