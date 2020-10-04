from PIL import Image, ImageDraw, ImageFont

from raid_monitor.sensors.cpu_temperature import Temperature, TEMPERATURE_STATE
from raid_monitor.settings import font_path


def draw(black: Image, red: Image, data: Temperature):
    draw_black = ImageDraw.Draw(black)
    draw_red = ImageDraw.Draw(red)

    font = ImageFont.truetype(font_path, 20)

    if data.state == TEMPERATURE_STATE.GOOD:
        canvas = draw_black
    else:
        canvas = draw_red

    if data.state in (TEMPERATURE_STATE.GOOD, TEMPERATURE_STATE.BAD):
        canvas.text((150, 20), f"{data.value:>4}°C", font=font, fill=0, anchor='right')
