from units.base_unit import BaseUnit

class BaseConverter:
    """
    Abstract base class for all converters.
    """
    def __init__(self, units: list[BaseUnit]):
        self.units = units

    def convert(self, value: str, from_unit: str, to_unit: str) -> str:
        """
        Convert the value from one unit to another.
        Must be implemented by each subclass.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def get_unit(self, name: str) -> BaseUnit | None:
        return next((unit for unit in self.units if unit.name == name), None)
