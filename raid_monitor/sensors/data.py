from raid_monitor.sensors.cpu_temperature import CpuTemperatureSensor
from raid_monitor.sensors.disk import DiskSensor


def prepare_data():
    return {
        'disk': DiskSensor().get_data(),
        'temperature': CpuTemperatureSensor().get_data()
    }
