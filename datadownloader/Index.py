import numpy as np 
import pandas as pd 
from .scrappers import yahoofinance

class Index:
    def __init__(self, ticker):
        self.ticker = '%5E' + ticker
        self.__info = None
        self.__history = None
        self.__period = None
        self.__interval = None
        
    def get_info(self):
        if self.__info is None:
            self.__info, self.__history = yahoofinance.get_data(self.ticker, return_info=True)
        
        return self.__info
    
    def get_history(self, period='max', interval='1d'):
        if self.__history is None or self.__period != period or self.__interval != interval:
            self.__info, self.__history = yahoofinance.get_data(self.ticker, period=period, interval=interval, return_info=True)
            self.__period = period
            self.__interval = interval

        return self.__history