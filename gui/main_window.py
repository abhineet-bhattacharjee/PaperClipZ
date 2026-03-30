import customtkinter as ctk
from gui.clipboard_card import ClipboardCard


class MainWindow(ctk.CTk):
    def __init__(self, paperclipz):
        super().__init__()

        self.paperclipz = paperclipz
        self.cards = []

        self.title("PaperClipZ")
        self.geometry("800x600")
        self.minsize(600, 400)

        self._setup_ui()

        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def _setup_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))

        title_label = ctk.CTkLabel(
            self.header_frame,
            text="📋 PaperClipZ",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")

        self.search_entry = ctk.CTkEntry(
            self.header_frame,
            placeholder_text="Search clipboard...",
            width=300,
            height=40
        )
        self.search_entry.pack(side="right")

        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            corner_radius=12
        )
        self.scrollable_frame.pack(fill="both", expand=True)

        self.footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.sort_mode_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"Sort mode: {self.paperclipz.get_sort_mode().title()}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.sort_mode_label.pack(side="left")

        self.total_items_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"Total items: {self.paperclipz.get_total_items()} items",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.total_items_label.pack(side="left", padx=20)

        pinned_count = self.paperclipz.get_pinned_count()
        if pinned_count > 0:
            self.pinned_count_label = ctk.CTkLabel(
                self.footer_frame,
                text=f"Pinned: {pinned_count} items",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            self.pinned_count_label.pack(side="left")
        else:
            self.pinned_count_label = None

        self.hotkey_label = ctk.CTkLabel(
            self.footer_frame,
            text="⌨️ Ctrl+1-0: Paste | Ctrl+P: Pin",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.hotkey_label.pack(side="right")

    def clear_cards(self):
        pass

    def show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        self.withdraw()
