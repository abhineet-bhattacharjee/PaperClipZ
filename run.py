import threading
import customtkinter as ctk

from app import PaperClipZ
from gui.main_window import MainWindow
from gui.tray import TrayIcon

if __name__ == "__main__":
    paperclipz = PaperClipZ()
    window = MainWindow(paperclipz)

    tray = TrayIcon(window)

    tray_thread = threading.Thread(target=tray.run, daemon=True)
    tray_thread.start()

    cli_thread = threading.Thread(target=paperclipz.run, daemon=True)
    cli_thread.start()

    window.mainloop()
