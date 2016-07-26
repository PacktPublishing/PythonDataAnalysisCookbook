import numpy as np
import pandas as pd


STOCKS = ['AAPL', 'INTC', 'MSFT', 'KO', 'DIS', 'MCD', 'NKE', 'IBM']


def log_rets(close):
    return np.diff(np.log(close))


def log_to_simple(rets):
    return np.exp(rets) - 1


def merge_sp500(stock, sp500):
    return pd.merge(left=stock, right=sp500,
                    right_index=True, left_index=True,
                    suffixes=('_stock', '_sp500')).dropna()
