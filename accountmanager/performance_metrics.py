import numpy as np 
import pandas as pd 
from itertools import groupby, chain

N_VALS = [252, 52, 12, 1] # Trading days, weeks, months, year in a year

# Returns
def annualised_return(returns, N=252):
    return returns.mean() * N

# Sharpe
def annualised_sharpe(returns, N=252):
    return np.sqrt(N) * returns.mean() / returns.std()

def equity_sharpe(returns, risk_free_rate=0.05):
    excess_daily_ret = returns - risk_free_rate/252
    return annualised_sharpe(excess_daily_ret, N=252)

def market_neutral_sharpe(returns, benchmark_returns):
    net_ret = (returns - benchmark_returns)/2.0
    return annualised_sharpe(net_ret)

# Drawdowns
def drawdown(ts):    
    drawdown_df = pd.DataFrame({'TS': ts})
    drawdown_df['Peak'] = ts.cummax()
    drawdown_df['Drawdown'] = drawdown_df['Peak'] - ts
    drawdown_df['Drawdown %'] = drawdown_df['Drawdown'] / drawdown_df['Peak']
    drawdown_df['Duration'] = list(chain.from_iterable((np.arange(len(list(j)))+1).tolist() if i==1 \
                         else [0]*len(list(j)) for i, j in groupby(drawdown_df['Drawdown'] != 0)))

    max_drawdown = drawdown_df['Drawdown %'].max()
    max_drawdown_duration = drawdown_df['Duration'].max()

    return drawdown_df, max_drawdown, max_drawdown_duration
