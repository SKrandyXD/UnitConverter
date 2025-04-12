from converters.linear_converter import LinearConverter
from units.linear_unit import LinearUnit

class AreaConverter(LinearConverter):
    def __init__(self):
        units = [
            LinearUnit("m2", "Square Meter", 1),
            LinearUnit("km2", "Square Kilometer", 1_000_000),
            LinearUnit("cm2", "Square Centimeter", 0.0001),
            LinearUnit("mm2", "Square Millimeter", 0.000001),
            LinearUnit("ha", "Hectare", 10_000),
            LinearUnit("acre", "Acre", 4046.86),
            LinearUnit("in2", "Square Inch", 0.00064516),
            LinearUnit("ft2", "Square Foot", 0.092903),
            LinearUnit("yd2", "Square Yard", 0.836127),
            LinearUnit("mi2", "Square Mile", 2_589_988)
        ]
        super().__init__(units)
