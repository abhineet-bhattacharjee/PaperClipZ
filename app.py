import pyperclip
import keyboard

import os
import time
import json
import hashlib
import math
from datetime import datetime, timedelta
from colorama import init, Fore, Style


class PaperClipZ:
    def __init__(self, history_file: str = 'history.json', config_file: str = 'config.json', interval: float = 1.0) -> None:
        init(autoreset=True)
        config = self._load_config(config_file)

        self.history_file: str = history_file
        self.interval: float = config.get('interval', interval)
        self.sort_mode: str = config.get('sort_mode', 'last_copied')
        self.newline: bool = config.get('newline', True)
        self.history: list[dict] = self._load_history()

        try:
            self.last_text: str = pyperclip.paste()
        except:
            self.last_text: str = ''

    def _load_config(self, config_file: str):
        if not os.path.exists(config_file):
            return {}

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def _compute_hash(self, text: str):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def _find_entry_by_hash(self, text_hash: str):
        for entry in self.history:
            if entry.get('id') == text_hash:
                return entry
        return None

    def _calculate_score(self, entry: dict):
        now = datetime.now()

        created = entry.get('created_at')
        last_pasted = entry.get('last_pasted_at')
        last_copied = entry.get('last_copied_at', created)

        if last_pasted:
            timestamp = last_pasted
        elif last_copied:
            timestamp = last_copied
        else:
            timestamp = created

        last_activity = self._parse_timestamp(timestamp)
        if last_activity and last_activity != datetime.min:
            hours_ago = (now - last_activity).total_seconds() / 3600
            recency_score = math.exp(-hours_ago / 24)
        else:
            recency_score = 0.0

        paste_count = entry.get('paste_count', 0)
        frequency_score = math.log(paste_count + 1)

        total_score = (recency_score * 10) + (frequency_score * 2 * recency_score)

        return total_score

    def _sort_items(self, limit: int = 10):
        if self.sort_mode == 'last_copied':
            sorted_history = sorted(
                self.history,
                key=lambda entry: self._parse_timestamp(
                    e.get('last_copied_at') or e.get('created_at'), ''),
                reverse=True
            )
            return sorted_history[:limit]
        else:
            sorted_history = sorted(
                self.history,
                key=lambda entry: self._calculate_score(entry),
                reverse=True
            )
            return sorted_history[:limit]

    def _parse_timestamp(self, timestamp: str | None):
        if not timestamp:
            return datetime.min
        try:
            dt = datetime.fromisoformat(timestamp_str)
            return dt
        except (ValueError, TypeError):
            return datetime.min

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
            print(f'{Fore.RED}Error saving history: {e}')

    def _add_entry(self, text: str) -> None:
        text_hash = self._compute_hash(text)
        existing_entry = self._find_entry_by_hash(text_hash)

        if existing_entry:
            self.history.remove(existing_entry)
            existing_entry['last_copied_at'] = datetime.now().isoformat(timespec='seconds')
            existing_entry['copy_count'] += 1

            self.history.append(existing_entry)
            print(f'{Fore.GREEN}UPDATE LOG: (copied {existing_entry["copy_count"]} times(s)): {text.strip()[:100]}{"..." if len(text) > 100 else ""}')
        else:
            entry = {
                'id': text_hash,
                'text': text,
                'created_at': datetime.now().isoformat(timespec='seconds'),
                'last_copied_at': datetime.now().isoformat(timespec='seconds'),
                'last_pasted_at': None,
                'copy_count': 1,
                'paste_count': 0
            }
            self.history.append(entry)
            print(f'{Fore.LIGHTGREEN_EX}SAVE LOG {len(self.history)}: {text.strip()[:100]}{"..." if len(text) > 100 else ""}')

        self._save_history()

    def _paste_entry(self, index: int):
        if not self.history:
            print(f"{Fore.RED}No history to paste from.")
            return

        recent_history = self._sort_items(limit=10)

        if index >= len(recent_history):
            print(f"{Fore.YELLOW}Invalid index for pasting. Only {len(recent_history)} items available.")
            return

        text_to_paste = recent_history[index]['text']
        text_to_paste += '\r\n' if not text_to_paste.endswith(('\n', '\r\n')) and self.newline else ''

        self.last_text = text_to_paste
        pyperclip.copy(text_to_paste)

        entry_id = recent_history[index]['id']
        for entry in self.history:
            if entry['id'] == entry_id:
                entry['last_pasted_at'] = datetime.now().isoformat(timespec='seconds')
                entry['paste_count'] = entry.get('paste_count', 0) + 1
                break

        self._save_history()

        keyboard.send('ctrl+v')

        print(f'{Fore.BLUE}PASTED [{index}]: {text_to_paste.strip()[:100]}{"..." if len(text_to_paste) > 100 else ""}')

    def _hotkeys(self):
        for i in range(1, 10):
            keyboard.add_hotkey(f'ctrl+{i}', lambda idx=i - 1: self._paste_entry(idx), suppress=True)

        keyboard.add_hotkey('ctrl+0', lambda idx=9: self._paste_entry(idx), suppress=True)

        print(f'{Fore.CYAN}Hotkeys registered:')
        print(f'{Fore.CYAN}  Ctrl+1 = Most recent')
        print(f'{Fore.CYAN}  Ctrl+2 = 2nd most recent')
        print(f'{Fore.CYAN}  ...')
        print(f'{Fore.CYAN}  Ctrl+0 = 10th most recent\n')

    def run(self) -> None:
        print(f'{Fore.CYAN}Clipboard logger started... (Ctrl+C to trigger)')
        self._hotkeys()

        try:
            while True:
                try:
                    text: str = pyperclip.paste()
                except:
                    print(f'{Fore.RED}Clipboard access failed, retrying...')
                    time.sleep(self.interval)
                    continue

                if text and text != self.last_text:
                    self._add_entry(text)
                    self.last_text = text
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print(f'{Fore.CYAN}\nClipboard logger stopped.')


if __name__ == '__main__':
    app = PaperClipZ()
    app.run()
