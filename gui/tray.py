import pystray
from PIL import Image, ImageDraw


def create_tray_icon():
    width = 64
    height = 64

    image = Image.new('RGB', (width, height), (30, 144, 255))
    dc = ImageDraw.Draw(image)

