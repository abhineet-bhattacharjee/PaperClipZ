import customtkinter as ctk


class ClipboardCard(ctk.CTkFrame):
    def __init__(self, parent, text="Example Clipboard Text", **kwargs):
        super().__init__(
            parent,
            corner_radius = 10,
            fg_color=('gray90', 'gray13'),
            **kwargs
        )