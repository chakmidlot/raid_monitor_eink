from datetime import datetime

from PIL import ImageDraw, ImageFont

from raid_monitor.settings import font_path


def draw(black, red):
    now = datetime.now()
    time = now.strftime('%H:%M')
    font = ImageFont.truetype(font_path, 18)

    drawblack = ImageDraw.Draw(black)
    drawblack.text((165, 0), time, font=font, fill=0)
