import logging
import time

from raid_monitor import settings
from raid_monitor.driver import driver
from raid_monitor.sensors.data import prepare_data
from raid_monitor import picture


logger = logging.getLogger(__name__)


def main():
    with driver() as draw:
        while True:

            data = prepare_data()
            black, red = picture.build_images(data)
            draw(black, red)

            time.sleep(settings.REFRESH_TIME)


if __name__ == '__main__':
    main()
