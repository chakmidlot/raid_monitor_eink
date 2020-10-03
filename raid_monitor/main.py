#!/usr/bin/python
# -*- coding:utf-8 -*-
import dataclasses
import json
import logging
import time
import os

from PIL import Image, ImageDraw, ImageFont

from raid_monitor.checker.disk import mock, get_data
from raid_monitor.lib import epd2in13b_V3
from raid_monitor.picture import screen

logging.basicConfig(level=logging.DEBUG)


def main():
    epd = epd2in13b_V3.EPD()
    epd.init()

    try:
        logging.info("init and Clear")
        i = 0

        while True:
            data = {
                'disk': get_data(),
            }

            logging.info(data)

            epd.init()

            i += 1
            if i == 10:
                epd.Clear()
                i = 0

            black, red = screen.draw(data)
            epd.display(epd.getbuffer(black), epd.getbuffer(red))

            logging.info("Goto Sleep...")
            epd.sleep()

            time.sleep(600)

    finally:
        epd2in13b_V3.epdconfig.module_exit()
        epd.Dev_exit()


if __name__ == '__main__':
    main()
