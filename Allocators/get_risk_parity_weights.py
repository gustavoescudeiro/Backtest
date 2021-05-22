from Allocators.core_risk_parity import *

def get_weights_rp(signal = None, prices = None, long_and_short = False, window = 222):
    w = window
    returns = prices.pct_change()

    if long_and_short == False:
        long_position = {}
        for i in signal.index:
            all_positions = signal.loc[i, :]
            lp = all_positions[all_positions == 1].index.to_list()
            long_position[i] = lp

        dic_long = {}
        for i in range(w, len(returns.index) + 1):
            df_sub = returns.iloc[(i - w + 1):i - 1]
            df_long = df_sub[long_position[df_sub.index[0]]]
            d_long = get_weight(df_long)
            dic_long[df_long.index[-1]] = d_long

        df_long = pd.concat(dic_long, axis=0)
        df_long = pd.DataFrame(df_long).reset_index()
        df_long.rename(columns={'level_0': 'date'}, inplace=True)
        df_long = df_long.pivot(index='date', columns='ticker', values='weight')

    return(df_long)





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
