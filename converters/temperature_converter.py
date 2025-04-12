from converters.base_converter import BaseConverter
from units.base_unit import BaseUnit

class TemperatureConverter(BaseConverter):
    """
    Converter for temperature units (Celsius, Fahrenheit, Kelvin).
    """
    def __init__(self):
        units = [
            BaseUnit("Celsius", "The Celsius scale, also known as the Centigrade scale, is used to measure temperature."),
            BaseUnit("Fahrenheit", "The Fahrenheit scale is primarily used in the United States to measure temperature."),
            BaseUnit("Kelvin", "The Kelvin scale is an absolute temperature scale used in science and engineering.")
        ]
        super().__init__(units)

    def convert(self, value: str, from_unit: str, to_unit: str) -> str:
        """
        Convert temperature from one unit to another.
        """

        try:
            numeric_value = float(value.strip()) if value.strip() else 0.0
        except ValueError:
            raise ValueError("Value must be a valid number string.")

        if not self.get_unit(from_unit) or not self.get_unit(to_unit):
            raise ValueError(f"Invalid unit: {from_unit} or {to_unit} not found in factors.")

        if from_unit == to_unit:
            return numeric_value

        # Convert to Kelvin first
        if from_unit == "Celsius":
            temp_in_kelvin = numeric_value + 273.15
        elif from_unit == "Fahrenheit":
            temp_in_kelvin = (numeric_value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin":
            temp_in_kelvin = numeric_value

        # Now convert from Kelvin to the target unit
        if to_unit == "Celsius":
            return temp_in_kelvin - 273.15
        elif to_unit == "Fahrenheit":
            return (temp_in_kelvin - 273.15) * 9/5 + 32
        elif to_unit == "Kelvin":
            return temp_in_kelvin
        else:
            raise ValueError(f"Unsupported temperature unit: {to_unit}")
