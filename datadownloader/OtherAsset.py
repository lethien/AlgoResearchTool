import pandas as pd 
from .scrappers.quandl_client import QuandlClient
from .scrappers import utils, yahoofinance

class Index:
    def __init__(self, ticker):
        self.ticker = '%5E' + ticker        
        self.__history = None
        self.__freq = None
        self.__freq_dict = {'daily': '1d', 'weekly': '1wk', 'monthly': '1mo'}
        
    def get_history(self, freq='daily'):
        if self.__history is None or self.__freq != freq:
            self.__info, self.__history = yahoofinance.get_data(self.ticker, period='max', interval=self.__freq_dict[freq], return_info=True)
            self.__freq = freq

        return self.__history

#https://blog.quandl.com/api-for-commodity-data?utm_source=google&utm_medium=organic&utm_campaign=&utm_content=tag/commodities
class Commodity:
    def __init__(self, commodity=None, code=None):
        self.quandl_client = QuandlClient()
        if code is None:
            if commodity is not None:
                self.commodity = commodity
                self.commodity_code = utils.get_commodity_code(commodity)
            else:
                raise ValueError("Either commodity name or code is required")
        else:
            self.commodity_code = code
            self.commodity = utils.get_commodity_name(code)
            
        self.__history = None
        self.__freq = 'daily'
    
    def get_history(self, freq='daily'):
        if self.__history is None or self.__freq != freq:
            indicator_history = self.quandl_client.get_data('CHRIS', self.commodity_code, freq=freq)            
            self.__history = indicator_history
            self.__freq = freq
        return self.__history