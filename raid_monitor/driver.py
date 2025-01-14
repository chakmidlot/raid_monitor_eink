import logging
from contextlib import contextmanager

from raid_monitor.lib import epd2in13b_V3


logger = logging.getLogger(__name__)


@contextmanager
def driver():
    epd = epd2in13b_V3.EPD()

    logger.info("init and Clear")
    epd.init()
    epd.Clear()

    try:
        i = 0

        def draw(black, red):
            nonlocal i

            epd.init()

            i += 1
            if i == 10:
                epd.Clear()
                i = 0

            epd.display(epd.getbuffer(black), epd.getbuffer(red))

            logger.info("Goto Sleep...")
            epd.sleep()

        yield draw

    finally:
        epd.Dev_exit()
