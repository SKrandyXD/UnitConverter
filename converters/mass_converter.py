from converters.linear_converter import LinearConverter
from units.linear_unit import LinearUnit

class MassConverter(LinearConverter):
    def __init__(self):
        units = [
            LinearUnit("g", "Gram", 1),
            LinearUnit("kg", "Kilogram", 1000),
            LinearUnit("ton", "Ton (metric)", 1_000_000),
            LinearUnit("lb", "Pound", 453.592),
            LinearUnit("oz", "Ounce", 28.3495),
            LinearUnit("stone", "Stone (UK)", 6350.29)
        ]
        super().__init__(units)
