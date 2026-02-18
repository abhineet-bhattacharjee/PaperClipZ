import customtkinter as ctk


class ClipboardCard(ctk.CTkFrame):
    def __init__(self, parent, text="Example Clipboard Text", **kwargs):
        super().__init__(
            parent,
            corner_radius = 10,
            fg_color=('gray90', 'gray13'),
            **kwargs
        )

        self.preview = ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=15),
            wraplength=600,
            justify='left',
            anchor='w',
        )
        self.preview.pack(fill='x', padx=15, pady=12)