import pyperclip
import keyboard
import time


def paste_text(text: str):
    pyperclip.copy(text)
    keyboard.send("ctrl+v")
    time.sleep(0.05)