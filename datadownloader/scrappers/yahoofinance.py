import numpy as np 
import pandas as pd 
import yfinance as yf

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
def get_data(ticker, period='max', interval='1d', return_info=False):
    ticker_obj = yf.Ticker(ticker)  
    histoty_data = ticker_obj.history(period=period, interval=interval, auto_adjust=False)
    if return_info:
        info_data = format_info(ticker_obj.info)
        return info_data, histoty_data
    else:
        return histoty_data

def format_info(info_dict):
    info_list = [(key, info_dict[key]) for key in info_dict.keys()]
    info_df = pd.DataFrame(info_list)
    info_df.columns = ['Field', 'Value']
    info_df.set_index('Field', inplace=True)
    return info_df