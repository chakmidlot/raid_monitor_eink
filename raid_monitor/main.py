import logging
import time

from raid_monitor import settings
from raid_monitor.driver import driver
from raid_monitor.sensors.data import prepare_data
from raid_monitor.picture import screen


logger = logging.getLogger(__name__)


def main():
    with driver() as draw:
        while True:

            data = prepare_data()
            logger.info(data)
            draw(*screen.build_images(data))

            time.sleep(settings.REFRESH_TIME)


if __name__ == '__main__':
    main()
