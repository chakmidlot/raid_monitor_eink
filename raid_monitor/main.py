import logging
import time

from raid_monitor.driver import driver
from raid_monitor.sensors.data import prepare_data
from raid_monitor.picture import screen

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def main():
    with driver() as draw:
        while True:

            data = prepare_data()
            logging.info(data)
            draw(*screen.build_images(data))

            time.sleep(600)


if __name__ == '__main__':
    main()
