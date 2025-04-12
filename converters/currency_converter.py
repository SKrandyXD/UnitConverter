from converters.linear_converter import LinearConverter
from api.currency_api import CurrencyAPI
from units.linear_unit import LinearUnit

class CurrencyConverter(LinearConverter):
    def __init__(self):
        try:
            self.currency_api = CurrencyAPI()
        except Exception:
            raise

        self.currency_api.update_rates()
        factors = self.currency_api.get_rates()
        units = [LinearUnit(name=key, description=key, factor=value) for key, value in factors.items()]
        super().__init__(units)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        if not self.get_unit(from_unit) or not self.get_unit(to_unit):
            raise ValueError("Invalid or unsupported currency.")

        # Convert value to USD (base currency)
        value_in_usd = value / self.get_unit(from_unit).factor

        # Convert value from USD to the target currency
        result = value_in_usd * self.get_unit(to_unit).factor

        return round(result, 2)