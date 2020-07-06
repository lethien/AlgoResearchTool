import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from scipy.stats import norm
from datetime import datetime as dt

# Detect mean-version by testing if time-series is random walk
def random_walk_test_adfuller(ts, maxlag=None, regression='ct', significant_level='5%'):
    adfuller_result = adfuller(ts, maxlag=maxlag, regression=regression)    
    is_random_walk = adfuller_result[4][significant_level] <= adfuller_result[0]
    return is_random_walk

def random_walk_test_adfuller_interpretation(adf_result):
    if adf_result:
        return "Is a Geometric Brownian Motion random walk"
    else:
        return "Is not a Geometric Brownian Motion random walk"

# Detect mean-version by testing if time-series is station
def stationary_test_hurst(ts):
    np_ts = np.array(ts)
    lags = range(2, 100)
    tau = [np.sqrt(np.std(np.subtract(np_ts[lag:], np_ts[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    
    return poly[0] * 2.0

def stationary_test_hurst_interpretation(h_result):
    if h_result < 0.5:
        return 'Time series is mean reverting'
    elif h_result == 0.5:
        return 'Time series is GBM random walk'
    else:
        return 'Time series is trending'

# Stationary test of pair
def get_hedge_ratio(ts1, ts2):
    model = sm.OLS(ts1, ts2)
    res = model.fit()
    return res.params[0]

def random_walk_test_cointegrate_adfuller(ts1, ts2, verbose=False):
    hedge_ratio = get_hedge_ratio(ts1, ts2)
    residuals = ts1 - ts2 * hedge_ratio
    
    if verbose:
        fig = plt.figure(figsize=(15,15), constrained_layout=True)
        gs = fig.add_gridspec(2,2)
        
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(ts1)
        ax1.plot(ts2)
        
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.scatter(ts1, ts2)
        
        ax3 = fig.add_subplot(gs[1, :])
        ax3.plot(residuals)
        
        plt.show()
    
    is_random_walk = random_walk_test_adfuller(residuals)
    
    if verbose:
        print("The time-series pair is a random walk:", is_random_walk)
        
    return is_random_walk, hedge_ratio

# Value at Risk
def VaR(Porfolio_value, confidence=0.99, returns):
    mu = returns.mean()
    sigma = returns.std()
    alpha = norm.ppf(1-confidence, mu, sigma)
    return Porfolio_value - Porfolio_value * (alpha + 1)