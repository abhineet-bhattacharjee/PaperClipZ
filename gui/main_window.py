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
        self.header = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.footer = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.footer.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))

    def show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        self.withdraw()
