import os

from PIL import Image

from raid_monitor.picture import resources


def draw(black: Image, red):
    pic = Image.open(os.path.join(resources, 'image.bmp'))
    black.paste(pic)
