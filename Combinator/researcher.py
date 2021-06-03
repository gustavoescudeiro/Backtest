import pandas as pd
import numpy as np
from Engine.Backtester import *
from Performance.performance import *
from Signals.get_signal_momentum import *
from Allocators.handler import *



import seaborn as sns
from matplotlib import pyplot as plt

prices = pd.read_pickle(r"../Data/equity_only.pkl")
ibov = pd.read_pickle(r"../Data/ibov.pkl").pct_change()
risk_free = pd.read_pickle(r"../Data/cdi.pkl")
prices = prices.loc[ibov.index]

cdi_returns = (1 + risk_free/100)**(1/252) - 1
cdi_returns.columns = ['cdi_return']

lista_percentil = [10, 20, 30, 40, 50, 60, 70, 80, 90]
lista_window = [[22, 22*2], [22, 22*3], [22, 22*4], [22, 22*5], [22, 22*6]]
list_model = ['risk_parity', '1/n']
list_rebal_freq = ['m']

combinacoes = []
for j in list_model:
    for i in lista_percentil:
        for k in lista_window:
            for m in list_rebal_freq:
                list_param = [i, k[0], k[1], j, m]
                combinacoes.append(list_param)

print(combinacoes)

resultados = []
for combinacao in combinacoes:

    sinal = get_final_df(prices, percentile = combinacao[0],
                         window_up = combinacao[1],
                         window_down = combinacao[2])

    l_wgt = generate_weights(signal = sinal, prices = prices, long_and_short = False, model = combinacao[3], compute_freq = combinacao[4], window = 365)
    resultado = backtest([prices, l_wgt], long_and_short = False, rebal_freq = 'm')
    resumo = summary_perfomance(resultado[0][['total_aum']], cdi_returns)
    resultados.append(resumo)

list_sharpes = []
for i in range(len(resultados)):
    list_sharpes.append(resultados[i][resultados[i].index == "Annual Sharpe Ratio"].iloc[0][0])

summary_df = pd.concat([pd.DataFrame(combinacoes, columns = ['percentil', 'window_up', 'window_down', 'allocator_model', 'rebal_frequency']),
            pd.DataFrame(list_sharpes, columns = ['annual_sharpe_ratio'])], axis = 1)

print('finished')