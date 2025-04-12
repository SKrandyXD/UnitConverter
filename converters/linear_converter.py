from converters.base_converter import BaseConverter
from units.linear_unit import LinearUnit

class LinearConverter(BaseConverter):
    """
    A converter class for linear unit conversions where units are related by a constant factor.
    (e.g., mass, speed, length, etc.)
    """
    def __init__(self, units: list[LinearUnit]):
        super().__init__(units)

    def convert(self, value: str, from_unit: str, to_unit: str) -> str:
        """
        Convert the value from one unit to another using a linear conversion factor.
        Assumes that the `factor` dictionary contains the conversion factor to a base unit.
        Accepts value as a string and parses it to a float.
        """
        try:
            numeric_value = float(value.strip()) if value.strip() else 0.0
        except ValueError:
            raise ValueError("Value must be a valid number string.")

        if not self.get_unit(from_unit) or not self.get_unit(to_unit):
            raise ValueError(f"Invalid unit: {from_unit} or {to_unit} not found in factors.")

        if from_unit == to_unit:
            return str(numeric_value)

        return str(numeric_value * (self.get_unit(from_unit).factor / self.get_unit(to_unit).factor))
