import numpy as np
import pandas as pd 
import quandl
from . import utils

class QuandlClient:
    def __init__(self, api_key=None):
        if api_key is None:
            default_api_key = utils.get_api_key('Quandl')
            if default_api_key is None:
                print('Warning: No Quandl API Key found. Some functionalities can be limitted.')
            else:
                quandl.ApiConfig.api_key = default_api_key
        else:
            quandl.ApiConfig.api_key = api_key
    
    # valid freqs: daily|weekly|monthly|quarterly|annual
    def get_data(self, dataset, code, freq='daily'):
        data = quandl.get("{}/{}".format(dataset, code), collapse=freq)
        return data
    
    def get_table(self, dataset, table, code):
        data = quandl.get_table('{}/{}'.format(dataset, table), ticker=code)
        return data