import numpy as np 
import pandas as pd 

# Kelly Formula
def kelly_criterion(returns, risk_free_rate=0.05, N=252):
    sharpe = equity_sharpe(returns, risk_free_rate)
    growth = risk_free_rate/N + sharpe**2 / 2
    leverage = (returns.mean() - risk_free_rate/N) / (returns.std() ** 2)
    return growth*N, leverage