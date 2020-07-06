import numpy as np
import pandas as pd 
import requests
import os

def get_ticker_short_name(ticker):    
    tickers = get_stock_ticker_and_name()
    name = tickers[tickers['symbol'] == ticker].iloc[0]['short_name']
    return name

def get_stock_ticker_and_name():
    ticker_meta_data_file = os.path.join(get_datadownloader_dir(), 'data', 'meta-data', 'tickers_with_name.csv')
    def shotern_name(name):
        name = name.split(' INC')[0]
        name = name.split(' CORP')[0]
        name = name.split(' LTD')[0]
        name = name.lower()
        name = name.replace('\'s', '')
        name = name.replace(' - ', '-')
        name = name.replace(' & ', '-')
        name = name.replace(' ', '-')
        return name

    try:
        tickers = pd.read_csv(ticker_meta_data_file)
    except Exception as e:
        r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
        tickers = pd.DataFrame(r.json())
        tickers = tickers[['symbol', 'name']]
        tickers = tickers[tickers['name'] != '']
        tickers['short_name'] = tickers['name'].apply(shotern_name)
        tickers.to_csv(ticker_meta_data_file, index=False)
    finally:
        return tickers

def get_currency_exchange_code(symbol):    
    exchange_meta_data_file = os.path.join(get_datadownloader_dir(), 'data', 'meta-data', 'fred_usd_exchange_rate.csv')
    exchanges = pd.read_csv(exchange_meta_data_file)
    code = exchanges[exchanges['symbol'] == symbol].iloc[0]['code']
    return code

def get_commodity_code(commodity_name):    
    commodities_meta_data_file = os.path.join(get_datadownloader_dir(), 'data', 'meta-data', 'commodities_code.csv')
    commodities = pd.read_csv(commodities_meta_data_file)    
    code = commodities[commodities['name'] == commodity_name].iloc[0]['code']
    return code

def get_commodity_name(commodity_code):    
    commodities_meta_data_file = os.path.join(get_datadownloader_dir(), 'data', 'meta-data', 'commodities_code.csv')
    commodities = pd.read_csv(commodities_meta_data_file)    
    name = commodities[commodities['code'] == commodity_code].iloc[0]['name']
    return name

def get_datadownloader_dir():
    current_file_dir = get_current_file_dir()
    return os.path.join(current_file_dir, '..')

def get_current_file_dir():
    return os.path.dirname(os.path.realpath(__file__))

def get_api_key(service):
    api_key_meta_data_file = os.path.join(get_datadownloader_dir(), 'data', 'meta-data', 'api_keys.csv')
    keys = pd.read_csv(api_key_meta_data_file)
    try:
        key = keys[keys['service'] == service].iloc[0]['key']
    except Exception as e:
        key = None
    finally:
        return key