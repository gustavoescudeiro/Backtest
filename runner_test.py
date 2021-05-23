import pandas as pd
import numpy as np
from Engine.Backtester import *
from Performance.performance import *
from Allocators.get_one_over_n_weights import *
from Allocators.core_risk_parity import *
from Signals.get_signal_momentum import *
import seaborn as sns
from matplotlib import pyplot as plt

prices = pd.read_pickle(r"Data/equity_only.pkl")
ibov = pd.read_pickle(r"Data/ibov.pkl").pct_change()
risk_free = pd.read_pickle(r"Data/cdi.pkl")
prices = prices.loc[ibov.index]

cdi_returns = (1 + risk_free/100)**(1/252) - 1
cdi_returns.columns = ['cdi_return']


#l_wgt = get_weights(get_final_df(prices, percentile = 20,
#                                     window_up = 5,
#                                     window_down = 122), long_and_short = False)

sinal = get_final_df(prices, percentile = 20,
                                     window_up = 5,
                                     window_down = 122)

l_wgt = get_weights_rp(signal = sinal, prices = prices, long_and_short = False, window = 220)

resultado = backtest([prices, l_wgt], long_and_short = False, rebal_freq = 'm')

resumo = summary_perfomance(resultado[0][['total_aum']], cdi_returns)
cum_returns_plot(resultado[0][['total_aum']].pct_change(), [ibov, cdi_returns])

weights_heatmap(l_wgt, 2021)
print('finished')