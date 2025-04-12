from converters.length_converter import LengthConverter
from converters.time_converter import TimeConverter

class SpeedConverter():
    def __init__(self):
        self.length_converter = LengthConverter()
        self.time_converter = TimeConverter()

    def convert(self, value: float | int, length_from_unit: str, length_to_unit: str,  time_from_unit: str, time_to_unit: str) -> float:
        length_value = float(self.length_converter.convert(str(1), length_from_unit, length_to_unit))
        time_value = float(self.time_converter.convert(str(1), time_from_unit, time_to_unit))
        return value * (length_value / time_value)
