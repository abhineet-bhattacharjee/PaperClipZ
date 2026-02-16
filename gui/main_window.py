import customtkinter as ctk

class MainWindow(ctk.CTk):
    def __init__(self, paperclipz):
        super().__init__()

        self.paperclipz = paperclipz

        self.title("PaperClipZ")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._setup_ui()
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def _setup_ui(self):
        header_label = ctk.CTkLabel(
            self,
            text="📋 PaperClipZ",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_label.pack(pady=20)

        placeholder_label = ctk.CTkLabel(
            self,
            text="Window is working!\nThis will show clipboard items later.",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        placeholder_label.pack(pady=50)

    def show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        self.withdraw()
