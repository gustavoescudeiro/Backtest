import pandas as pd
import numpy as np


def set_position(valor, upper_percentile, lower_percentile):
    posicao = 0
    if valor > upper_percentile:
        posicao = 1
    elif valor < lower_percentile:
        posicao = -1
    else:
        posicao = 0
    return posicao


def get_signal(df, percentile=30):
    df_betas = df.copy()

    cols = df_betas.columns
    # Usar np.percentil (garanta que não há nans)
    df_betas['upper_percentile'] = df_betas.apply(lambda x: np.nanpercentile(x, 100 - percentile), axis=1)
    df_betas['lower_percentile'] = df_betas.apply(lambda x: np.nanpercentile(x, percentile), axis=1)

    df_pos = df_betas.copy()
    for col in cols:
        df_pos[col] = df_pos.apply(lambda x: set_position(x[col], x['upper_percentile'], x['lower_percentile']), axis=1)

    df_pos.drop(columns=['upper_percentile', 'lower_percentile'], inplace=True)

    return df_pos


def get_final_df(df, window_up=22, window_down=60, percentile=30):
    signal = df.apply(func=lambda x: x.shift(window_up) / x.shift(window_down) - 1, axis=0)
    signal = get_signal(signal, percentile)
    return (signal)