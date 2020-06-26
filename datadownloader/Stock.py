import numpy as np 
import pandas as pd 
from .scrappers import yahoofinance, macrotrends

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.__info = None
        self.__history = None
        self.__period = None
        self.__interval = None
        self.__balance_sheet = None
        self.__income_statement = None
        self.__cash_flow_statement =None
        self.__financial_ratios = None
    
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

    def get_balance_sheet(self, freq='Q'):
        if self.__balance_sheet is None:
            self.__balance_sheet = macrotrends.get_financial_data(self.ticker, statement='balance-sheet', freq=freq)
        
        return self.__balance_sheet
    
    def get_income_statement(self, freq='Q'):
        if self.__income_statement is None:
            self.__income_statement = macrotrends.get_financial_data(self.ticker, statement='income-statement', freq=freq)
        
        return self.__income_statement

    def get_cash_flow_statement(self, freq='Q'):
        if self.__cash_flow_statement is None:
            self.__cash_flow_statement = macrotrends.get_financial_data(self.ticker, statement='cash-flow-statement', freq=freq)
        
        return self.__balance_sheet

    def get_financial_ratios(self, freq='Q'):
        if self.__financial_ratios is None:
            self.__financial_ratios = macrotrends.get_financial_data(self.ticker, statement='financial-ratios', freq=freq)
        
        return self.__financial_ratios