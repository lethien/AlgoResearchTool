import pandas as pd 
from .scrappers.quandl_client import QuandlClient
from .scrappers.alphavantage_client import AlphaVantageFOREXClient
from .scrappers import utils

# https://www.quandl.com/data/FRED-Federal-Reserve-Economic-Data/documentation?anchor=data-organization
class EconomyIndicator:
    def __init__(self, indicator_code):
        self.quandl_client = QuandlClient()
        self.indicator_code = indicator_code
        self.__freq = 'daily'
        self.__history = None
    
    def get_history(self, freq = 'daily'):
        if self.__history is None or self.__freq != freq:
            indicator_history = self.quandl_client.get_data('FRED', self.indicator_code, freq=freq)            
            self.__history = indicator_history
            self.__freq = freq
        return self.__history

class Currency:
    def __init__(self, exchange_currency, base_currency='USD'):
        self.quandl_client = QuandlClient()
        self.alphavantage_client = AlphaVantageFOREXClient()
        self.__freq = 'daily'
        self.base_currency = base_currency
        self.exchange_currency = exchange_currency
        self.exchange_symbol = "{0}/{1}: {0} to {1}".format(base_currency, exchange_currency)
        self.__history = None
    
    def get_history(self, freq='daily'):
        if self.__history is None or self.__freq != freq:            
            currency_exchange_history = self.alphavantage_client.get_data(self.base_currency, self.exchange_currency, freq=freq)            
            self.__history = currency_exchange_history
            self.__freq = freq

        return self.__history

    def __get_history_from_quandl(self):
        if self.__history is None or self.__freq != freq:
            exchange_currency_code = utils.get_currency_exchange_code(self.exchange_currency)
            currency_exchange_history = self.quandl_client.get_data('FRED', exchange_currency_code)
            if self.base_currency != 'USD':
                base_currency_code = utils.get_currency_exchange_code(self.base_currency)
                base_exchange_history = self.quandl_client.get_data('FRED', base_currency_code)
                currency_exchange_history =  currency_exchange_history / base_exchange_history
            
            self.__history = currency_exchange_history
            self.__freq = freq
        return self.__history

# https://www.quandl.com/data/USTREASURY-US-Treasury?keyword=yield
class TreasuryYield:
    def __init__(self):
        self.quandl_client = QuandlClient()
        self.__freq = 'daily'
        self.__history = None
    
    def get_history(self, freq = 'daily'):
        if self.__history is None or self.__freq != freq:
            yield_history = self.quandl_client.get_data('USTREASURY', 'YIELD', freq=freq)            
            self.__history = yield_history
            self.__freq = freq
        return self.__history