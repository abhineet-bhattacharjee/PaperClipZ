import pyperclip
import keyboard
import time
from colorama import init, Fore
from .clipboard import ClipboardManager
from .pinning import PinManager
from utils.helpers import compute_hash


class CLI:
    def __init__(self, clipboard_manager: ClipboardManager, pin_manager: PinManager,
                 newline: bool = True, interval: float = 0.1):
        init(autoreset=True)
        self.clipboard_manager = clipboard_manager
        self.pin_manager = pin_manager
        self.newline = newline
        self.interval = interval
        self.last_hash = ""
        self.is_pasting = False
        self.running = False

        try:
            initial_text = pyperclip.paste()
            if initial_text:
                self.last_hash = compute_hash(initial_text)
        except Exception:
            pass

    def _paste_entry(self, index: int):
        items = self.clipboard_manager.get_sorted_items(10)

        if index >= len(items):
            print(f"{Fore.RED}No item at position {index + 1}")
            return

        entry = items[index]
        original_text = entry["text"]

        text_to_paste = original_text
        if self.newline and not original_text.endswith(("\n", "\r\n")):
            text_to_paste += "\r\n"

        self.is_pasting = True
        self.last_hash = compute_hash(text_to_paste)

        pyperclip.copy(text_to_paste)
        keyboard.send("ctrl+v")

        self.clipboard_manager.storage.update_paste_stats(entry)

        display = original_text.strip()[:80]
        count = entry["paste_count"]
        pin_indicator = "📌 " if entry.get("pinned") else ""
        print(f"{Fore.BLUE}PASTED [{index + 1}]: {pin_indicator}pasted {count}x | {display}")

        time.sleep(0.05)
        self.is_pasting = False

    def _toggle_pin_current(self):
        try:
            current_text = pyperclip.paste()
            self.pin_manager.toggle_pin(current_text)
        except:
            pass

    def _setup_hotkeys(self):
        for i in range(10):
            keyboard.add_hotkey(
                f"ctrl+{(i + 1) % 10}",
                lambda idx=i: self._paste_entry(idx),
                suppress=True,
            )

        keyboard.add_hotkey("ctrl+p", self._toggle_pin_current, suppress=True)

        print(f"{Fore.CYAN}Hotkeys: Ctrl+1-0 (paste), Ctrl+P (pin/unpin)")
        print(f"{Fore.CYAN}Sort mode: {self.clipboard_manager.sort_mode}")

    def stop(self):
        self.running = False

    def run(self):
        print(f"{Fore.CYAN}PaperClipZ started (Ctrl+C to stop)")
        self._setup_hotkeys()
        self.running = True

        try:
            while self.running:
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

                current_hash = compute_hash(text)
                if current_hash != self.last_hash:
                    self.clipboard_manager.storage.add_entry(text, current_hash)
                    self.last_hash = current_hash

                time.sleep(self.interval)
        except KeyboardInterrupt:
            print(f"{Fore.CYAN}\nPaperClipZ stopped")