import pandas as pd
import numpy as np
from Backtester import *
from performance import *
from get_one_over_n_weights import *
from get_signal_momentum import *
import seaborn as sns
from matplotlib import pyplot as plt

prices = pd.read_pickle("./equity_only.pkl")
ibov = pd.read_pickle("./equity.pkl")[['^BVSP']].pct_change()
risk_free = pd.read_pickle("./cdi.pkl")

cdi_returns = (1 + risk_free/100)**(1/252) - 1
cdi_returns.columns = ['cdi_return']


l_wgt = get_weights(get_final_df(prices, percentile = 30,
                                     window_up = 22,
                                     window_down = 251), long_and_short = False)

resultado = backtest([prices, l_wgt], long_and_short = False, rebal_freq = 'm')

resumo = summary_perfomance(resultado[0][['total_aum']], cdi_returns)
cum_returns_plot(resultado[0][['total_aum']].pct_change(), [ibov, cdi_returns])
print('teste')