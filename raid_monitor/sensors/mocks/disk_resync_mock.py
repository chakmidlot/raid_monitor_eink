from raid_monitor.sensors.disk import DiskSensor


class MockResyncDiskSensor(DiskSensor):

    def get_disk_state(self):
        return '''Personalities : [raid1] 
md0 : active raid1 sdb1[0] sda1[2]
      3906851776 blocks super 1.2 [2/1] [_U]
      [===>.................]  recovery = 15.4% (602929152/3906851776) finish=528.5min speed=104177K/sec
      bitmap: 4/30 pages [16KB], 65536KB chunk

unused devices: <none>'''


    def get_disk_space(self):
        return '''Filesystem     1G-blocks  Used Available Use% Mounted on
/dev/root           117G    2G      111G   2% /
devtmpfs              4G    0G        4G   0% /dev
tmpfs                 4G    0G        4G   0% /dev/shm
tmpfs                 4G    1G        4G   1% /run
tmpfs                 1G    1G        1G   1% /run/lock
tmpfs                 4G    0G        4G   0% /sys/fs/cgroup
/dev/mmcblk0p1        1G    1G        1G  22% /boot
/dev/md0           3667G  901G     2580G  26% /media/RAID1
tmpfs                 1G    0G        1G   0% /run/user/1000'''


if __name__ == '__main__':
    print(MockResyncDiskSensor().get_data())
