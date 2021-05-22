from Allocators.core_risk_parity import *







prices = pd.read_pickle(r"../Data/equity_only.pkl")
ibov = pd.read_pickle(r"../Data/ibov.pkl").pct_change()
prices = prices.loc[ibov.index]

returns = prices.pct_change()




from Signals.get_signal_momentum import *


sinal = get_final_df(prices, percentile = 20,
                                     window_up = 5,
                                     window_down = 122)

pesos = get_weights_rp(signal = sinal, prices = prices, long_and_short = False, window = 222)
print('finished')
