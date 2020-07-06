import numpy as np
import pandas as pd 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from . import utils

class AlphaVantageClient:
    def __init__(self, api_key=None):
        if api_key is None:
            default_api_key = utils.get_api_key('AlphaVantage')
            if default_api_key is None:
                raise ValueError('No AlphaVantage API Key found.')
            else:
                self.ts = TimeSeries(key=default_api_key, output_format='pandas')
        else:
            self.ts = TimeSeries(key=api_key, output_format='pandas')
    
    def get_data(self, symbol, freq='daily', adjusted=True, interval='15min', outputsize='full'):
        """ Return time series in pandas formet.
        Keyword Arguments:
            symbol:  the symbol for the equity we want to get its data
            freq: frequency of data, supported values are 'daily', 'weekly', 'monthly' (default 'daily'). Currently not support for 'intraday'
            adjusted: adjust the OHLC value (default True)
            interval:  time interval between two conscutive values, used when freq is intraday
                supported values are '1min', '5min', '15min', '30min', '60min'
                (default '15min')
            outputsize:  The size of the call, supported values are
                'compact' and 'full; the first returns the last 100 points in the
                data series, and 'full' returns the full-length intraday times
                series, commonly above 1MB (default 'compact')
        """
        key = '{}-{}'.format(freq, adjusted)
        
        # elif key == 'intraday-True': 
        #     data, _ = self.ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
        # elif key == 'intraday-False': 
        #     data, _ = self.ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
        
        if key == 'daily-True': 
            data, _ = self.ts.get_daily_adjusted(symbol=symbol, outputsize=outputsize)
        elif key == 'daily-False': 
            data, _ = self.ts.get_daily(symbol=symbol, outputsize=outputsize)
        elif key == 'weekly-True': 
            data, _ = self.ts.get_weekly_adjusted(symbol=symbol)
        elif key == 'weekly-False': 
            data, _ = self.ts.get_weekly(symbol=symbol)
        elif key == 'monthly-True': 
            data, _ = self.ts.get_monthly_adjusted(symbol=symbol)
        elif key == 'monthly-False': 
            data, _ = self.ts.get_monthly(symbol=symbol)
        else:
            raise Warning('Freq: {} or Adjusted: {} is not valid. Default to Daily Adjusted.')
            data, _ = self.ts.get_daily_adjusted(symbol=symbol, outputsize=outputsize)
        
        if freq == 'intraday':
            data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        else:
            columns_name = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits']
            data.columns = columns_name[:len(data.columns)]

        data = data.rename(index={'date': 'Date'})
        
        return data.sort_index(ascending=True)

    def get_latest_data(self, symbol):
        """ Return the latest price and volume information for a security of your choice 
        Keyword Arguments:
            symbol:  the symbol for the equity we want to get its data
        """
        data, _ = self.ts.get_quote_endpoint(symbol=symbol)
        
        columns_name = ['Open', 'High', 'Low', 'Price', 'Volume', 'Date', 'Previous Close', 'Change', 'Change Pct']
        data = data.iloc[:, 1:]
        data.columns = columns_name
        data = data.set_index(['Date'])

        return data
    
class AlphaVantageFOREXClient:
    def __init__(self, api_key=None):
        if api_key is None:
            default_api_key = utils.get_api_key('AlphaVantage')
            if default_api_key is None:
                raise ValueError('No AlphaVantage API Key found.')
            else:
                self.ts = ForeignExchange(key=default_api_key, output_format='pandas')
        else:
            self.ts = ForeignExchange(key=api_key, output_format='pandas')
    
    def get_data(self, from_currency, to_currency, freq='daily', interval='15min', outputsize='full'):
        """ Return time series in pandas formet.
        Keyword Arguments:
            from_currency:  The currency you would like to get the exchange rate
            for. It can either be a physical currency or digital/crypto currency.
            to_currency: The destination currency for the exchange rate.
            It can either be a physical currency or digital/crypto currency.
            freq: frequency of data, supported values are 'daily', 'weekly', 'monthly' (default 'daily'). Currently not support for 'intraday'          
            interval:  time interval between two conscutive values, used when freq is intraday
                supported values are '1min', '5min', '15min', '30min', '60min'
                (default '15min')
            outputsize:  The size of the call, supported values are
                'compact' and 'full; the first returns the last 100 points in the
                data series, and 'full' returns the full-length intraday times
                series, commonly above 1MB (default 'compact')
        """
        
        # if freq == 'intraday': 
        #     data, _ = self.ts.get_currency_exchange_intraday(from_symbol=from_currency, to_symbol=to_currency, interval=interval, outputsize=outputsize)
        
        if freq == 'daily': 
            data, _ = self.ts.get_currency_exchange_daily(from_symbol=from_currency, to_symbol=to_currency, outputsize=outputsize)
        elif freq == 'weekly': 
            data, _ = self.ts.get_currency_exchange_weekly(from_symbol=from_currency, to_symbol=to_currency, outputsize=outputsize)
        elif freq == 'monthly': 
            data, _ = self.ts.get_currency_exchange_monthly(from_symbol=from_currency, to_symbol=to_currency, outputsize=outputsize)        
        else:
            raise Warning('Freq: {}  is not valid. Default to Daily.')
            data, _ = self.ts.get_currency_exchange_daily(from_symbol=from_currency, to_symbol=to_currency, outputsize=outputsize)
        
        data.columns = ['Open', 'High', 'Low', 'Close']        
        data = data.rename(index={'date': 'Date'})

        return data.sort_index(ascending=True)

    def get_latest_data(self, from_currency, to_currency):
        """ Return the latest price and volume information for a exchange of your choice 
        Keyword Arguments:
            from_currency:  The currency you would like to get the exchange rate
            for. It can either be a physical currency or digital/crypto currency.
            to_currency: The destination currency for the exchange rate.
            It can either be a physical currency or digital/crypto currency.
        """
        data, _ = self.ts.get_currency_exchange_rate(from_currency=from_currency, to_currency=to_currency)
        
        data = data.iloc[:, [0, 2, 4, 5, 7, 8]]
        columns_name = ['From', 'To', 'Rate', 'Date', 'Bid', 'Ask']
        data.columns = columns_name
        data = data.set_index(['Date'])

        return data