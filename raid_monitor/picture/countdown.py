from PIL import Image, ImageDraw, ImageFont

from raid_monitor.sensors.cpu_temperature import Temperature, TEMPERATURE_STATE
from raid_monitor.settings import font_path


def draw(black: Image, red: Image, data: str):
    draw_black = ImageDraw.Draw(black)

    font = ImageFont.truetype(font_path, 30)

    canvas = draw_black

    canvas.text((160, 60), data, font=font, fill=0, align='right')
