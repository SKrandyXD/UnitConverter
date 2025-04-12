from converters.linear_converter import LinearConverter
from units.linear_unit import LinearUnit

class TimeConverter(LinearConverter):
    def __init__(self):
        units = [
            LinearUnit("Second", "Second", 1),
            LinearUnit("Minute", "Minute", 60),
            LinearUnit("Hour", "Hour", 3600),
            LinearUnit("Day", "Day", 86400),
            LinearUnit("Week", "Week", 604800),
            LinearUnit("Month", "Month (30.44 days)", 2629746),
            LinearUnit("Year", "Year (365.25 days)", 31556952)
        ]
        super().__init__(units)
