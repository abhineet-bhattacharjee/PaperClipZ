import customtkinter as ctk
from app import PaperClipZ


class MainWindow(ctk.CTk):
    def __init__(self, paperclipz):
        super().__init__()

        self.paperclipz = paperclipz

        self.title("PaperClipZ")
        self.geometry("800x600")
        self.minsize(600, 400)

        self._setup_layout()
        self._setup_ui()

        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header - fixed
        self.grid_rowconfigure(1, weight=1)  # Content - expands
        self.grid_rowconfigure(2, weight=0)  # Footer - fixed

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

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.footer = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.footer.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            self.header,
            text="PaperClipZ - Clipboard Manager",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")

        ctk.CTkLabel(
            self.content,
            text="Clipboard items will appear here",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(expand=True)

        ctk.CTkLabel(
            self.footer,
            text=f"Sort mode: {self.paperclipz.clipboard_manager.sort_mode}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="left")

    def show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        self.withdraw()
