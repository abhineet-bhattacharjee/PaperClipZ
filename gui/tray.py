import pystray
from PIL import Image, ImageDraw


def create_tray_icon():
    width = 64
    height = 64

    image = Image.new('RGB', (width, height), (30, 144, 255))
    dc = ImageDraw.Draw(image)

    dc.rectangle([12, 16, 52, 48], fill='white', outline='black', width=2)
    dc.rectangle([20, 8, 44, 20], fill='white', outline='black', width=2)

    return image


class TrayIcon:
    def __init__(self, window):
        self.icon = None
        self.window = window

    def create_menu(self):
        return pystray.Menu(
            pystray.MenuItem("Open PaperClipZ", self.on_open),
            pystray.MenuItem("Exit", self.on_exit)
        )

    def on_open(self):
        if self.window:
            self.window.after(0, self.window.show_window)

    def on_exit(self):
        if self.window:
            self.window.after(0, self.window.destroy)

    def run(self):
        self.icon = pystray.Icon(
            "PaperClipZ",
            create_tray_icon(),
            "PaperClipZ - Clipboard Manager",
            menu=self.create_menu()
        )
        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()