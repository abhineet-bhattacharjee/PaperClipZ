from colorama import Fore
from .storage import Storage
from utils.helpers import compute_hash


class PinManager:
    def __init__(self, storage: Storage):
        self.storage = storage

    def toggle_pin(self, text: str) -> None:
        if not text:
            return

        text_hash = compute_hash(text)
        entry = self.storage.find_entry(text_hash)

        if not entry:
            print(f"{Fore.YELLOW}Item not in history")
            return

        if entry.get("pinned"):
            entry["pinned"] = False
            entry["pin_order"] = None

            self._compact_pin_order()

            display = text.strip()[:80]
            print(f"{Fore.YELLOW}UNPINNED: {display}")
        else:
            max_pin_order = max(
                (e.get("pin_order", -1) for e in self.storage.history if e.get("pinned")),
                default=-1
            )
            entry["pinned"] = True
            entry["pin_order"] = max_pin_order + 1
            display = text.strip()[:80]
            print(f"{Fore.YELLOW}PINNED: {display}")

        self.storage.save()

    def _compact_pin_order(self):
        pinned_items = [e for e in self.storage.history if e.get("pinned")]
        pinned_items.sort(key=lambda e: e.get("pin_order", 0))

        for idx, entry in enumerate(pinned_items):
            entry["pin_order"] = idx