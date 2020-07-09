import numpy as np 
import pandas as pd 
from . import performance_metrics

class Porfolio:
    def __init__(self, starting_capital):
        self.__starting_capital = starting_capital
        self.__capital = starting_capital
        self.__holding = {}
        self.__value_history = []
        self.__trading_history = []
        
    def get_current_capital(self):
        return self.__capital

    def __calculate_current_total_value(self, assets_current_price_dict):
        capital_value = self.__capital

        holding_value = 0
        for (k, v) in self.__holding.items():
            holding_value += v * assets_current_price_dict[k]['Price']
        
        total_value = capital_value + holding_value
        
        return total_value

    def update_value_history(self, date, assets_current_price_dict):
        total_value = self.__calculate_current_total_value(assets_current_price_dict)
        self.__value_history.append((date, total_value))
        return True

    def get_value_history(self):
        df = pd.DataFrame(data = self.__value_history)
        df.columns = ['Date', 'Value']
        df = df.set_index(['Date'])
        return df.sort_index(ascending=True)
    
    def get_tickers_in_porfolio(self):
        tickers = self.__holding.items()
        
        return pd.DataFrame(data=tickers)
    
    def update_trading_history(self, date, ticker, quantity, price):
        if ticker not in self.__holding.keys():
            self.__holding[ticker] = 0
        
        ticker_quantity = self.__holding[ticker]
        if (ticker_quantity + quantity) < 0:
            raise ValueError('Quantity of {} in porfolio: {}. Change quantity: {}. Update quantity will be negative.'.format(ticker, ticker_quantity, quantity))

        capital = self.__capital
        change_capital = quantity * price
        if (capital - change_capital) < 0:
            raise ValueError('Capital in porfolio: {}. Change quantity: {}. Update quantity will be negative.'.format(capital, change_capital))

        self.__trading_history.append((date, ticker, quantity))
        self.__holding[ticker] += quantity
        self.__capital -= change_capital
        return True

    def get_trading_history(self):
        df = pd.DataFrame(data = self.__trading_history)
        df.columns = ['Date', 'Ticker', 'Quantity']
        df = df.set_index(['Date'])
        return df.sort_index(ascending=True)

    def get_porfolio_performance(self, risk_free_rate=0.05, N=252):        
        performance = {}

        value_history = self.get_value_history()['Value']
        performance['Value History'] = value_history
        value_history_ror = value_history.pct_change()
        performance['Rate of Return History '] = value_history_ror

        performance['Current Value'] = value_history.iloc[-1]
        performance['Total Growth'] = (performance['Current Value'] - self.__starting_capital) / self.__starting_capital

        performance['Annualized Rate of Return'] = performance_metrics.annualised_return(value_history_ror)

        performance['Sharpe Ratio'] = performance_metrics.equity_sharpe(value_history_ror, risk_free_rate)

        drawdown_df, max_drawdown, max_drawdown_duration = performance_metrics.drawdown(value_history)
        performance['Drawdowns'] = drawdown_df
        performance['Maximum Drawdown'] = max_drawdown
        performance['Maximum Drawdown Duration'] = max_drawdown_duration

        return performance
