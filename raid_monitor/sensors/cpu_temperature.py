import re
import subprocess
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from typing import Optional


class TEMPERATURE_STATE(Enum):
    GOOD = auto()
    BAD = auto()
    NOT_AVAILABLE = auto()


@dataclass
class Temperature:
    state: TEMPERATURE_STATE
    value: Optional[Decimal]


class CpuTemperatureSensor:

    def get_data(self):
        try:
            temp = self.parse_temperature(self.get_from_system())

            if temp >= 60:
                state = TEMPERATURE_STATE.BAD
            else:
                state = TEMPERATURE_STATE.GOOD

            return Temperature(state, temp)

        except Exception:
            return Temperature(TEMPERATURE_STATE.NOT_AVAILABLE, None)

    def parse_temperature(self, text):
        match = re.match("temp=([\-\d.]+)'C", text)

        if not match:
            raise Exception("Can't parse temperature")

        return Decimal(match.groups()[0])

    def get_from_system(self):
        process = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
        process.wait()

        if process.returncode != 0:
            raise Exception('df command failed')

        return process.stdout.read().decode()
