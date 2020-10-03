import logging
import re
import subprocess
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from raid_monitor import settings


logger = logging.getLogger(__name__)


class RAID_STATE(Enum):
    READY = auto()
    RESYNC = auto()
    ONE_DISK = auto()
    FAILED = auto()


@dataclass
class Disk:
    state: RAID_STATE
    size: Optional[float]
    used: Optional[float]
    resync: Optional[float]
    description: Optional[str]


class DiskSensor:

    def get_data(self):
        try:
            state, details = self.parse_mdstat(self.get_disk_state())
            space = self.parse_disk_space(self.get_disk_space())

            if state == RAID_STATE.FAILED or space is None:
                return Disk(state=RAID_STATE.FAILED, size=None, used=None, resync=None, description='No raid found')

            info = Disk(
                state=state,
                size=int(space['total']),
                used=int(space['used']),
                resync=details.get('percent'),
                description=None
            )

            logger.info(info)

            return info

        except Exception:
            logger.exception("Failed reading disk info")
            return Disk(
                state=RAID_STATE.FAILED,
                size=None,
                used=None,
                resync=None,
                description='Failed query'
            )

    def get_disk_state(self):
        process = subprocess.Popen(['cat', '/proc/mdstat'], stdout=subprocess.PIPE)
        process.wait()

        if process.returncode != 0:
            raise Exception('"cat /proc/mdstat" command failed')

        return process.stdout.read().decode()


    def get_disk_space(self):
        process = subprocess.Popen(['df', '-BG'], stdout=subprocess.PIPE)
        process.wait()

        if process.returncode != 0:
            raise Exception('df command failed')

        return process.stdout.read().decode()

    def parse_mdstat(self, text):
        regex = re.compile(rf'\n{settings.RAID} : active .+?\n\n', re.DOTALL)
        state = regex.search(text)

        if not state:
            return RAID_STATE.FAILED, {}

        state = state.group()

        sync = re.search(r'\[=.*>\.*]\s+'
                          '\w+ = (?P<percent>[\d.]+)% '
                          '\('
                              '(?P<synced>\d+)/'
                              '(?P<total>\d+)'
                          '\) '
                          'finish=(?P<ttl>[\w.]+) '
                          'speed=(?P<speed>[\w./]+)'
                         , state)
        if sync:
            sync_progress = sync.groupdict()
            return RAID_STATE.RESYNC, {
                'percent': float(sync_progress['percent']) / 100
            }

        sync = re.search(r'\d+ blocks super 1.2 \[2/1]', state)
        if sync:
            return RAID_STATE.ONE_DISK, {}

        sync = re.search(r'\d+ blocks super 1.2 \[2/2]', state)
        if sync:
            return RAID_STATE.READY, {}

        return RAID_STATE.FAILED, {}

    def parse_disk_space(self, text):
        regex = re.compile(
            rf'''
                /dev/{settings.RAID}\s+
                (?P<total>\d+)G\s+
                (?P<used>\d+)G\s+
                (?P<free>\d+)G\s+ 
                (?P<used_percent>\d+)%\s+
                (?P<mount>[/\w]+)''',
            re.VERBOSE)

        disk_line = regex.search(text)
        return disk_line and disk_line.groupdict()
