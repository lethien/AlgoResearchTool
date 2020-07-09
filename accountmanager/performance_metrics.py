import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from itertools import groupby, chain, product

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

# Confusion matrix Plot
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

# Porfolio performance plot
def plot_porfolio_performance(porfolio_perf):
    fig = plt.figure(figsize=(15,15), constrained_layout=True)
    gs = fig.add_gridspec(2,2)

    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(porfolio_perf['Value History'])

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(porfolio_perf['Drawdowns']['TS'])
    ax2.plot(porfolio_perf['Drawdowns']['Peak'])
    ax2.set_ylabel('Porfolio Value with Peaks')

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(porfolio_perf['Drawdowns']['Drawdown %'])
    ax3.set_ylabel('Drawdown %')

    plt.show()