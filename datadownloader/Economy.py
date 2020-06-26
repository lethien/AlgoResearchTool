import pandas as pd 
from .scrappers.quandl_client import QuandlClient
from .scrappers import utils, yahoofinance

# https://www.quandl.com/data/FRED-Federal-Reserve-Economic-Data/documentation?anchor=data-organization
class EconomyIndicator:
    def __init__(self, indicator_code):
        self.quandl_client = QuandlClient()
        self.indicator_code = indicator_code
        self.__history = None
    
    def get_history(self):
        if self.__history is None:
            indicator_history = self.quandl_client.get_data('FRED', self.indicator_code)            
            self.__history = indicator_history
        return self.__history

class Currency:
    def __init__(self, exchange_currency, base_currency='USD'):
        self.quandl_client = QuandlClient()
        self.base_currency = base_currency
        self.exchange_currency = exchange_currency
        self.exchange_symbol = "{0}/{1}: {0} to {1}".format(base_currency, exchange_currency)
        self.__history = None
    
    def get_history(self):
        if self.__history is None:
            exchange_currency_code = utils.get_currency_exchange_code(self.exchange_currency)
            currency_exchange_history = self.quandl_client.get_data('FRED', exchange_currency_code)
            if self.base_currency != 'USD':
                base_currency_code = utils.get_currency_exchange_code(self.base_currency)
                base_exchange_history = self.quandl_client.get_data('FRED', base_currency_code)
                currency_exchange_history =  currency_exchange_history / base_exchange_history
            
            self.__history = currency_exchange_history
        return self.__history

# https://www.quandl.com/data/USTREASURY-US-Treasury?keyword=yield
class TreasuryYield:
    def __init__(self):
        self.quandl_client = QuandlClient()
        self.__history = None
    
    def get_history(self):
        if self.__history is None:
            yield_history = self.quandl_client.get_data('USTREASURY', 'YIELD')            
            self.__history = yield_history
        return self.__history