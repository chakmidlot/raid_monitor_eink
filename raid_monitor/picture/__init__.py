import os

from PIL import Image

from raid_monitor import settings
from raid_monitor.picture import clock, disk, image, temperature
from raid_monitor.sensors.mocks.cpu_temperature_low import MockCpuTemperatureSensor
from raid_monitor.sensors.mocks.disk_resync_mock import MockResyncDiskSensor


def build_images(data):
    black = Image.new('1', (settings.EPD_WIDTH, settings.EPD_HEIGHT), 255)
    red = Image.new('1', (settings.EPD_WIDTH, settings.EPD_HEIGHT), 255)

    image.draw(black, red)
    clock.draw(black, red)
    disk.draw(black, red, data['disk'])
    temperature.draw(black, red, data['temperature'])

    return black, red


def combine_black_red_debug(black, red):
    WHITE = 0xffffff
    BLACK = 0x000000
    RED   = 0x0000ff

    colored = Image.new('RGB', (settings.EPD_WIDTH, settings.EPD_HEIGHT), WHITE)
    black_data = list(black.getdata())
    red_data = list(red.getdata())

    for i in range(settings.EPD_HEIGHT):
        for j in range(settings.EPD_WIDTH):
            if black_data[i * settings.EPD_WIDTH + j] == 0:
                colored.putpixel((j, i), BLACK)

            if red_data[i * settings.EPD_WIDTH + j] == 0:
                colored.putpixel((j, i), RED)

    return colored


if __name__ == '__main__':
    data = {
        'disk': MockResyncDiskSensor().get_data(),
        'temperature': MockCpuTemperatureSensor().get_data()
    }

    combine_black_red_debug(*build_images(data)).save('../../docs/result_image.jpg')
