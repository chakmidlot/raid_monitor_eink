from raid_monitor.sensors.cpu_temperature import CpuTemperatureSensor


class MockCpuTemperatureSensor(CpuTemperatureSensor):

    def get_from_system(self):
        return "temp=55.0'C"


if __name__ == '__main__':
    print(MockCpuTemperatureSensor().get_data())
