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

    def run(self):
        self.cli.run()
