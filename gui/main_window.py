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

       for i in range(5):
            card = ClipboardCard(
                self.scrollable_frame,
                text=f"Fake clipboard item #{i+1}\nThis is a preview of clipboard content"
            )
            card.pack(fill="x", pady=5)
            self.cards.append(card)

        self.footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 20))

    def show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        self.withdraw()