import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]")


EPD_HEIGHT = 104
EPD_WIDTH = 212

RAID = 'md0'
MOUNT = '/media/RAID1'

REFRESH_TIME = 600
