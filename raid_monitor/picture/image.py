import os

from PIL import Image

from raid_monitor.settings import resources


def draw(black: Image, red):
    pic = Image.open(os.path.join(resources, 'seal.bmp'))
    black.paste(pic)
