from converters.linear_converter import LinearConverter
from units.linear_unit import LinearUnit

class VolumeConverter(LinearConverter):
    """
    A converter for volume units using LinearUnit instances.
    """
    def __init__(self):
        units = [
            LinearUnit("m3", "Cubic Meter", 1),
            LinearUnit("L", "Liter", 0.001),
            LinearUnit("mL", "Milliliter", 0.000001),
            LinearUnit("gallon", "US Gallon", 0.00378541),
            LinearUnit("quart", "US Quart", 0.000946353),
            LinearUnit("pint", "US Pint", 0.000473176),
            LinearUnit("cup", "US Cup", 0.00024),
            LinearUnit("fluid oz", "US Fluid Ounce", 0.0000295735)
        ]
        
        super().__init__(units)
