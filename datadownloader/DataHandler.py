import numpy as np 
import pandas as pd 
from datetime import datetime
from .Stock import Stock
from .OtherAsset import Index, Commodity
from .Economy import EconomyIndicator, Currency, TreasuryYield

class DataHandler:
    def __init__(self):
        self.__trading_days = None
        self.__assets = {}  
        self.__assets_codes = []  

    def prepare_data(self, data_type, codes, columns, price_column, freq, get_fundamental=False, verbose=False):   
        for c in codes:
            if verbose:
                print('{} {} - Start'.format(data_type, c))

            if data_type == 'stock':            
                asset = Stock(c)
            elif data_type == 'index':
                asset = Index(c)
            elif data_type == 'commodity':
                asset = Commodity(c)
            elif data_type == 'economy':
                asset = EconomyIndicator(c)
            elif data_type == 'currency':
                currencies = c.split('/')
                asset = Currency(currencies[0], currencies[1])
            elif data_type == 'treasury':
                asset = TreasuryYield()

            history_data = asset.get_history(freq)

            if data_type == 'stock' and get_fundamental:
                fundamental_data = asset.get_fundamental_data()
                history_data = pd.concat([history_data, fundamental_data], axis=1)

            price_data = history_data[price_column].to_numpy()
            history_data = history_data[columns]
            history_data['Price'] = price_data

            history_data = history_data.dropna(how='all')

            history_data = history_data.fillna(method='ffill')
            history_data = history_data.fillna(method='bfill')

            self.__assets[c] = history_data
            self.__assets_codes.append(c)
            if self.__trading_days is None:
                self.__trading_days = history_data.index.to_numpy()
            else:
                self.__trading_days = np.append(self.__trading_days, history_data.index.to_numpy())
            self.__trading_days = np.sort(np.unique(self.__trading_days))

            if verbose:
                print('{} {} - Downloaded'.format(data_type, c))

    def get_updated_data(self, date=datetime.date(datetime.now()), nrows=1):
        latest = {}

        for code in self.__assets_codes:
            latest_data = self.__assets[code]
            
            if nrows == 1:
                latest_data = latest_data.iloc[latest_data.index.get_loc(date)]
            elif nrows > 1:
                latest_data = latest_data.iloc[latest_data.index.get_loc(date)-nrows+1 : latest_data.index.get_loc(date)+1]
            else:
                # return max data
                latest_data = latest_data.loc[:date]
            
            latest[code] = latest_data
        
        return latest

    def get_next_trading_date(self, current_date, n=1):        
        i, = np.where(self.__trading_days >= np.datetime64(current_date))
        if len(i) < n:            
            return None # latest date reached
        else:
            return self.__trading_days[i[0] + n]