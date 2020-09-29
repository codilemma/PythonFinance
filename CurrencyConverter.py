import requests


class CurrencyConverter:
    def __init__(self, symbols, API_KEY):
        self.API_KEY = API_KEY
        self.symbols = symbols
        self._symbols = ','.join([str(s) for s in symbols])
        r = requests.get(
            'https://openexchangerates.org/api/latest.json',
            params = {
                'app_id': self.API_KEY,
                'symbols': self._symbols,
                'show_alternative': 'true'
                }
            )
        self.rates_ = r.json()['rates']
        self.rates_['USD'] = 1
    def convert(self, value, symbol_from, symbol_to, round_output=True):
        try:
            x = (value
                * 1/self.rates_.get(symbol_from)
                * self.rates_.get(symbol_to))
            if round_output:
                return round(x, 2)
            else:
                return x
        except TypeError:
            print('Unavailable or invalid symbol')
            return None


# Use the currency converter class
#API_KEY = os.environ.get("OPX_KEY")
#c = CurrencyConverter(['CAD','USD'], API_KEY)
#
#print(c.convert(3000, 'CAD', 'USD'))
#print(c.convert(5000, 'USD', 'CAD'))