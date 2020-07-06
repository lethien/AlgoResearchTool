# Data scapped from MacroTrends (https://www.macrotrends.net/)
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
from datetime import datetime
import re
import os
from . import utils

LOGGER.setLevel(logging.WARNING)
BASE_URL = "https://www.macrotrends.net/stocks/charts"
FREQS = ['A', 'Q'] # 'Annual', 'Quarterly'
STATEMENTS = ['income-statement', 'balance-sheet', 'cash-flow-statement', 'financial-ratios']

def get_financial_data(ticker, statement='income-statement', freq='Q'):
    # Build the ULR
    short_name = utils.get_ticker_short_name(ticker)
    url = '{}/{}/{}/{}?freq={}'.format(BASE_URL, ticker, short_name, statement, freq)
    
    # Get data from built url
    data = get_macro_trends_data_from_url(url)
    return data

def get_macro_trends_data_from_url(url):
    # Create Headless Chrome Browser
    options = webdriver.ChromeOptions()
    options.add_argument('headless')    
    driver_file = os.path.join(utils.get_current_file_dir(), 'chromedriver_win32', 'chromedriver.exe')
    browser = webdriver.Chrome(driver_file, options=options)

    try:    
        # Get the webpage and parse for data
        browser.get(url)            
        data = browser.execute_script('return originalData')
        data = parse_data(data)
    except Exception as e:
        print('Failed to parse html: '+ str(e))
        data = None
    finally:
        browser.quit()
        return data

def parse_data_column(data_column):
    data_dates = []
    data_values = []

    for (k,v) in data_column.items():
        if k == 'field_name': # Parse field's name
            field_name = re.search('>(.+?)<', v).group(1)            
        elif k != 'popup_icon': # Parse data by date
            data_dates.append(datetime.strptime(k, '%Y-%m-%d'))
            try:
                data_val = float(v)
            except ValueError:
                data_val = None
            data_values.append(data_val)

    data_parsed = pd.DataFrame({'Date': data_dates, field_name: data_values})
    return data_parsed

def parse_data(data):
    data_dfs = []

    # Parse data for each field
    for data_column in data:
        data_parsed = parse_data_column(data_column)
        data_dfs.append(data_parsed)
    
    # Merge all into one data frame
    dataframe = data_dfs[0]
    for i in range(1, len(data_dfs)):
        dataframe = pd.merge(dataframe, data_dfs[i], on='Date', how='outer')
    
    return dataframe.set_index('Date')