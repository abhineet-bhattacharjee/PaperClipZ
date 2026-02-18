from .config import Config
from .storage import Storage
from .clipboard import ClipboardManager
from .pinning import PinManager
from .cli import CLI


class PaperClipZ:
    def __init__(
            self,
            history_file: str = "data/history.json",
            config_file: str = "data/config.json",
    ):
        self.config = Config(config_file)
        self.storage = Storage(history_file)

        interval = self.config.get("interval", 0.1)
        sort_mode = self.config.get("sort_mode", "smart")
        newline = self.config.get("newline", True)

        self.clipboard_manager = ClipboardManager(self.storage, sort_mode)
        self.pin_manager = PinManager(self.storage)
        self.cli = CLI(self.clipboard_manager, self.pin_manager, newline, interval)
        self.running = False

    def get_sort_mode(self) -> str:
        return self.clipboard_manager.sort_mode

    def get_total_items(self) -> int:
        return len(self.storage.history)

    def get_pinned_count(self) -> int:
        return len([e for e in self.storage.history if e.get("pinned")])

    def run(self):
        self.running = True
        self.cli.run()

    def stop(self):
        ...
