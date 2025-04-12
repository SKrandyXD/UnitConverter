from units.base_unit import BaseUnit

class LinearUnit(BaseUnit):
    def __init__(self, name: str, description: str | None, factor: float):
        super().__init__(name, description)
        self.factor = factor