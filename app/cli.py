import time
import keyboard
import pyperclip
from colorama import Fore

from app.core import PaperClipZ
from utils.helpers import compute_hash


def run_cli():
    app = PaperClipZ()

    # hotkeys
    for i in range(10):
        keyboard.add_hotkey(
            f"ctrl+{(i + 1) % 10}",
            lambda idx=i: app._paste_entry(idx),
            suppress=True,
        )

    keyboard.add_hotkey("ctrl+p", app._toggle_pin_current, suppress=True)

    print(f"{Fore.CYAN}PaperClipZ started (Ctrl+C to stop)")

    try:
        while True:
            try:
                text = pyperclip.paste()
            except Exception:
                time.sleep(app.interval)
                continue

            if not text or app.is_pasting:
                time.sleep(app.interval)
                continue

            current_hash = compute_hash(text)
            if current_hash != app.last_hash:
                app._add_entry(text, current_hash)
                app.last_hash = current_hash

            time.sleep(app.interval)

    except KeyboardInterrupt:
        print(f"{Fore.CYAN}\nPaperClipZ stopped")