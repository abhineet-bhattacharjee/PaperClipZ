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
