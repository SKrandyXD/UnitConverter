from converters.linear_converter import LinearConverter
from units.linear_unit import LinearUnit

class DataConverter(LinearConverter):
    def __init__(self):
        units = [
            LinearUnit("bit", "Bit", 1),
            LinearUnit("byte", "Byte", 8),
            LinearUnit("KB", "Kilobyte (1024 bytes)", 8 * 1024),
            LinearUnit("MB", "Megabyte (1024 KB)", 8 * 1024**2),
            LinearUnit("GB", "Gigabyte (1024 MB)", 8 * 1024**3),
            LinearUnit("TB", "Terabyte (1024 GB)", 8 * 1024**4),
            LinearUnit("PB", "Petabyte (1024 TB)", 8 * 1024**5)
        ]
        super().__init__(units)
