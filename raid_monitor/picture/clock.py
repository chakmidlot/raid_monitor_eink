from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from raid_monitor import picture, settings


def draw(black, red):
    now = datetime.now()
    time = now.strftime('%H:%M')
    font20 = ImageFont.truetype(picture.font_path, 18)

    drawblack = ImageDraw.Draw(black)
    drawblack.text((165, 0), time, font=font20, fill=0)


if __name__ == '__main__':
    black = Image.new('1', (settings.EPD_WIDTH, settings.EPD_HEIGHT), 255)
    red = Image.new('1', (settings.EPD_WIDTH, settings.EPD_HEIGHT), 255)

    draw(black, red)

    black.save('black.bmp')
    red.save('red.bmp')
