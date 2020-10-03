import re
import subprocess
from dataclasses import dataclass
from enum import Enum, auto

from raid_monitor import settings


class RAID_STATE(Enum):
    READY = auto()
    RESYNC = auto()
    ONE_DISK = auto()
    FAILED = auto()


@dataclass
class Disk:
    state: RAID_STATE
    size: float
    used: float
    resync: float
    description: str


def get_data():
    state, details = get_disk_state()
    space = get_disk_space()

    if state == RAID_STATE.FAILED or space is None:
        return Disk(state=RAID_STATE.FAILED, size=None, used=None, resync=None, description='No raid found')

    return Disk(
        state=state,
        size=int(space['total']),
        used=int(space['used']),
        resync=details.get('percent'),
        description=None
    )


def get_disk_state():
    process = subprocess.Popen(['cat', '/proc/mdstat'], stdout=subprocess.PIPE)
    process.wait()

    if process.returncode != 0:
        return RAID_STATE.FAILED, {}

    return parse_mdstat(process.stdout.read().decode())


def get_disk_space():
    process = subprocess.Popen(['df', '-BG'], stdout=subprocess.PIPE)
    process.wait()

    if process.returncode != 0:
        return

    return parse_disk_space(process.stdout.read().decode())


def parse_mdstat(text):
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


def parse_disk_space(text):
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


mock = {
    'failed': Disk(state=RAID_STATE.FAILED, size=None, used=None, resync=None, description='No raid found'),
    'resync': Disk(state=RAID_STATE.RESYNC, size=3.7, used=0.9, resync=0.115, description='One disk failed'),
    'ready': Disk(state=RAID_STATE.READY, size=3.7, used=1.1, resync=None, description='Resync ETA: 443m'),
    'one_disk': Disk(state=RAID_STATE.ONE_DISK, size=3.7, used=2, resync=None, description='Resync ETA: 443m'),
}


if __name__ == '__main__':
    syncing = '''Personalities : [raid1] 
md0 : active raid1 sdb1[0] sda1[2]
      3906851776 blocks super 1.2 [2/1] [_U]
      [===>.................]  recovery = 15.4% (602929152/3906851776) finish=528.5min speed=104177K/sec
      bitmap: 4/30 pages [16KB], 65536KB chunk

unused devices: <none>'''

    degraded = '''Personalities : [raid1] 
md0 : active raid1 sda1[2]
      3906851776 blocks super 1.2 [2/1] [_U]
      bitmap: 0/30 pages [0KB], 65536KB chunk

unused devices: <none>'''

    active = '''Personalities : [raid1] 
md0 : active raid1 sdb1[0] sda1[2]
      3906851776 blocks super 1.2 [2/2] [UU]
      bitmap: 0/30 pages [0KB], 65536KB chunk

unused devices: <none>'''

    print(parse_mdstat(syncing))


    df = '''/dev/md0           3667G  911G     2570G  27% /media/RAID1'''
    print(parse_disk_space(df))
