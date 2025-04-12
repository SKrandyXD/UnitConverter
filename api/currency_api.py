import requests

class CurrencyAPI:
    def __init__(self):
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.data = {}

    def update_rates(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error fetching currency rates: {e}")
        except Exception as e:
            raise ValueError(f"An error occurred while fetching the currency rates: {e}")

    def get_rates(self):
        return self.data.get('rates', {})
