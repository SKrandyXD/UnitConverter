from converters.linear_converter import LinearConverter
from units.linear_unit import LinearUnit

class LengthConverter(LinearConverter):
    def __init__(self):
        units = [
            LinearUnit("m", "Meter", 1),
            LinearUnit("km", "Kilometer", 1000),
            LinearUnit("cm", "Centimeter", 0.01),
            LinearUnit("mm", "Millimeter", 0.001),
            LinearUnit("mile", "Mile", 1609.34),
            LinearUnit("yard", "Yard", 0.9144),
            LinearUnit("foot", "Foot", 0.3048),
            LinearUnit("inch", "Inch", 0.0254),
            LinearUnit("nautical_mile", "Nautical Mile", 1852)
        ]
        super().__init__(units)
