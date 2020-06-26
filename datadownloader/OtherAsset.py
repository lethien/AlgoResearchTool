import pandas as pd 
from .scrappers.quandl_client import QuandlClient
from .scrappers import utils, yahoofinance

class Index:
    def __init__(self, ticker):
        self.ticker = '%5E' + ticker        
        self.__history = None
        self.__period = None
        self.__interval = None
        
    def get_history(self, period='max', interval='1d'):
        if self.__history is None or self.__period != period or self.__interval != interval:
            self.__info, self.__history = yahoofinance.get_data(self.ticker, period=period, interval=interval, return_info=True)
            self.__period = period
            self.__interval = interval

        return self.__history

#https://blog.quandl.com/api-for-commodity-data?utm_source=google&utm_medium=organic&utm_campaign=&utm_content=tag/commodities
class Commodity:
    def __init__(self, commodity):
        self.quandl_client = QuandlClient()
        self.commodity = commodity
        self.commodity_code = utils.get_commodity_code(commodity)
        self.__history = None
    
    def get_history(self):
        if self.__history is None:
            indicator_history = self.quandl_client.get_data('CHRIS', self.commodity_code)            
            self.__history = indicator_history
        return self.__history