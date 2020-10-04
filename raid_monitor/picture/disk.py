from PIL import Image, ImageDraw, ImageFont

from raid_monitor.sensors.disk import Disk, RAID_STATE
from raid_monitor.settings import font_path


def draw(black: Image, red: Image, data: Disk):
    draw_black = ImageDraw.Draw(black)
    draw_red = ImageDraw.Draw(red)

    font = ImageFont.truetype(font_path, 18)

    bar_width = 150

    if data.state == RAID_STATE.FAILED:
        draw_red.text((20, 0), "RAID IS FAILED", font=font, fill=0)
        return

    if data.state == RAID_STATE.ONE_DISK:
        bar_canvas = draw_red
    else:
        bar_canvas = draw_black

    bar_canvas.rectangle((5, 4, bar_width + 5, 16))
    used_bar = int(bar_width * data.used / data.size)
    bar_canvas.rectangle((5, 4, used_bar + 5, 16), 0)

    if data.state == RAID_STATE.RESYNC:
        resync_bar = int(bar_width * data.resync)
        draw_red.rectangle((5, 12, resync_bar + 5, 16), 0)

