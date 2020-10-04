import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(levelname)s] - [%(name)s] - [%(message)s]")


EPD_HEIGHT = 104
EPD_WIDTH = 212

RAID = 'md0'
MOUNT = '/media/RAID1'

REFRESH_TIME = 600

resources = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')

font_path = os.path.join(resources, 'Font.ttc')
