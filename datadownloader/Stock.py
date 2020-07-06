import numpy as np 
import pandas as pd 
from .scrappers.alphavantage_client import AlphaVantageClient
from .scrappers import macrotrends

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.avc = AlphaVantageClient()
        self.__history = None
        self.__frequency = None
        self.__balance_sheet = None
        self.__income_statement = None
        self.__cash_flow_statement =None
        self.__financial_ratios = None
        self.__balance_sheet_freq = None
        self.__income_statement_freq = None
        self.__cash_flow_statement_freq =None
        self.__financial_ratios_freq = None
        self.__funcdamental_data = None
        self.__funcdamental_data_freq = None
    
    def get_history(self, freq='daily'):
        if self.__history is None or self.__frequency != freq:
            self.__history = self.avc.get_data(self.ticker, freq=freq)
            self.__frequency = freq

        return self.__history

    def get_balance_sheet(self, freq='Q'):
        if self.__balance_sheet is None or self.__balance_sheet_freq != freq:
            self.__balance_sheet = macrotrends.get_financial_data(self.ticker, statement='balance-sheet', freq=freq)
            self.__balance_sheet_freq = freq
        
        return self.__balance_sheet
    
    def get_income_statement(self, freq='Q'):
        if self.__income_statement is None or self.__income_statement_freq != freq:
            self.__income_statement = macrotrends.get_financial_data(self.ticker, statement='income-statement', freq=freq)
            self.__income_statement_freq = freq
        
        return self.__income_statement

    def get_cash_flow_statement(self, freq='Q'):
        if self.__cash_flow_statement is None or self.__cash_flow_statement_freq != freq:
            self.__cash_flow_statement = macrotrends.get_financial_data(self.ticker, statement='cash-flow-statement', freq=freq)
            self.__cash_flow_statement_freq = freq
        
        return self.__cash_flow_statement

    def get_financial_ratios(self, freq='Q'):
        if self.__financial_ratios is None or self.__financial_ratios_freq != freq:
            self.__financial_ratios = macrotrends.get_financial_data(self.ticker, statement='financial-ratios', freq=freq)
            self.__financial_ratios_freq = freq
        
        return self.__financial_ratios

    def get_funcdamental_data(self, freq='Q'):
        if self.__funcdamental_data is None or self.__funcdamental_data_freq != freq:
            self.__funcdamental_data = pd.concat([
                self.get_balance_sheet(freq),
                self.get_income_statement(freq),
                self.get_cash_flow_statement(freq),
                self.get_financial_ratios(freq)
            ], axis=1)
            self.__funcdamental_data_freq = freq
        
        return self.__funcdamental_data

