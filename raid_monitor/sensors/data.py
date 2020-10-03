from raid_monitor.sensors.disk import DiskSensor


def prepare_data():
    return {
        'disk': DiskSensor().get_data(),
    }
