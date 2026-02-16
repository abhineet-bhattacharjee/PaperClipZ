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
