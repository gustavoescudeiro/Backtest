import pandas as pd
import numpy as np
from datetime import datetime


def backtest(dic_data, long_and_short=True, rebal_freq='M'):
    if long_and_short == False:

        prices = dic_data[0]
        l_wgt = dic_data[1]
        initial_ammount = 100
        returns = prices.pct_change()

        # fazemos isso para que o peso do dia anterior vá para o próximo dia.
        # Importante, pois quando pegarmos o primeiro dia de cada mês para rebalancear, os pesos serão do último dia do mês anterior
        l_wgt = l_wgt.shift(1)

        # fazemos isso para garantir que as primeiras linhas nao contenham somente NAN's
        # caso isso ocorresse, o backtest nao avancaria

        l_wgt.dropna(axis=0, how='all', inplace=True)

        long_ini_period = l_wgt.groupby(pd.DatetimeIndex(l_wgt.index).to_period(rebal_freq)).nth(0)
        long_ini_period.index = l_wgt.groupby(pd.DatetimeIndex(l_wgt.index).to_period(rebal_freq)).head(1).index

        qty = (long_ini_period.iloc[1] * initial_ammount / prices.loc[long_ini_period.index[1]])
        quota_value = (long_ini_period.iloc[1] * initial_ammount / prices.loc[long_ini_period.index[1]]) * prices.loc[
            long_ini_period.index[1]]

        dic_qty_long = {}
        dic_quota_value_long = {}
        dic_saldo_long = {}

        dic_qty_long[long_ini_period.index[1]] = qty
        dic_quota_value_long[long_ini_period.index[1]] = quota_value
        dic_saldo_long[long_ini_period.index[1]] = qty

        list_rebal_dates = long_ini_period.loc[
            long_ini_period.index[long_ini_period.index > quota_value.name][0:]].index

        k = 0
        for i in returns.index[returns.index > quota_value.name]:

            if k < len(list_rebal_dates) and i == list_rebal_dates[k]:
                print(str(i) + ' hora de rebalancear')
                list_prices = prices.index.to_list()
                position = list_prices.index(list_rebal_dates[k])
                position_yesterday = position - 1
                prices_in_the_day = prices.iloc[position_yesterday]
                qty_in_the_day = dic_qty_long[list(dic_qty_long.keys())[-1]]
                aum_in_the_day = (qty_in_the_day * prices_in_the_day)
                new_pos = long_ini_period.iloc[k]
                wgt_in_the_day = aum_in_the_day / aum_in_the_day.sum()
                new_wgt = long_ini_period.iloc[k + 2]
                aum_in_the_day = aum_in_the_day.sum()
                new_qty = new_wgt * aum_in_the_day / prices_in_the_day
                new_qty[np.isnan(new_qty)] = 0
                qty_in_the_day[np.isnan(qty_in_the_day)] = 0
                saldo = new_qty - qty_in_the_day
                qty = qty_in_the_day + saldo
                dic_qty_long[i] = qty
                quota_value = qty * prices_in_the_day  # verificar se é esse preço msm
                quota_value = (1 + returns.loc[i]) * quota_value
                dic_quota_value_long[i] = quota_value
                dic_saldo_long[i] = saldo
                print(aum_in_the_day)

                # multiplicando pelos retornos do dia
                quota_value = (1 + returns.loc[i]) * quota_value
                dic_quota_value_long[i] = quota_value
                dic_qty_long[i] = qty
                soma = quota_value.sum()

                k += 1


            else:
                quota_value = (1 + returns.loc[i]) * quota_value
                dic_quota_value_long[i] = quota_value
                dic_qty_long[i] = qty
                soma = quota_value.sum()
                print(i)

        df_quota_long = pd.DataFrame(pd.concat(dic_quota_value_long, axis=0)).reset_index()
        df_quota_long.rename(columns={'level_0': 'date', 0: 'quota'}, inplace=True)
        df_quota_long = df_quota_long.pivot(index='date', columns='ticker', values='quota')
        df_quota_long['total_aum'] = df_quota_long.sum(axis=1)

        df_saldo_long = pd.DataFrame(pd.concat(dic_saldo_long, axis=0)).reset_index()
        df_saldo_long.rename(columns={'level_0': 'date', 0: 'qty'}, inplace=True)
        df_saldo_long = df_saldo_long.pivot(index='date', columns='ticker', values='qty')
        df_saldo_long['total_qty'] = df_saldo_long.sum(axis=1)

        return (df_quota_long, df_saldo_long)

    else:

        prices = dic_data[0]
        l_wgt = dic_data[1]
        s_wgt = dic_data[2]
        initial_ammount = 100
        returns = prices.pct_change()

        # fazemos isso para que o peso do dia anterior vá para o próximo dia.
        # Importante, pois quando pegarmos o primeiro dia de cada mês para rebalancear, os pesos serão do último dia do mês anterior
        l_wgt = l_wgt.shift(1)
        s_wgt = s_wgt.shift(1)

        # fazemos isso para garantir que as primeiras linhas nao contenham somente NAN's
        # caso isso ocorresse, o backtest nao avancaria

        l_wgt.dropna(axis=0, how='all', inplace=True)
        s_wgt.dropna(axis=0, how='all', inplace=True)

        # Long
        long_ini_period = l_wgt.groupby(pd.DatetimeIndex(l_wgt.index).to_period(rebal_freq)).nth(0)
        long_ini_period.index = l_wgt.groupby(pd.DatetimeIndex(l_wgt.index).to_period(rebal_freq)).head(1).index

        qty = (long_ini_period.iloc[1] * initial_ammount / prices.loc[long_ini_period.index[1]])
        quota_value = (long_ini_period.iloc[1] * initial_ammount / prices.loc[long_ini_period.index[1]]) * prices.loc[
            long_ini_period.index[1]]

        dic_qty_long = {}
        dic_quota_value_long = {}
        dic_saldo_long = {}

        dic_qty_long[long_ini_period.index[1]] = qty
        dic_quota_value_long[long_ini_period.index[1]] = quota_value
        dic_saldo_long[long_ini_period.index[1]] = qty

        list_rebal_dates = long_ini_period.loc[
            long_ini_period.index[long_ini_period.index > quota_value.name][0:]].index

        k = 0
        for i in returns.index[returns.index > quota_value.name]:

            if k < len(list_rebal_dates) and i == list_rebal_dates[k]:
                print(str(i) + ' hora de rebalancear')
                list_prices = prices.index.to_list()
                position = list_prices.index(list_rebal_dates[k])
                position_yesterday = position - 1
                prices_in_the_day = prices.iloc[position_yesterday]
                qty_in_the_day = dic_qty_long[list(dic_qty_long.keys())[-1]]
                aum_in_the_day = (qty_in_the_day * prices_in_the_day)
                new_pos = long_ini_period.iloc[k]
                wgt_in_the_day = aum_in_the_day / aum_in_the_day.sum()
                new_wgt = long_ini_period.iloc[k + 2]
                aum_in_the_day = aum_in_the_day.sum()
                new_qty = new_wgt * aum_in_the_day / prices_in_the_day
                new_qty[np.isnan(new_qty)] = 0
                qty_in_the_day[np.isnan(qty_in_the_day)] = 0
                saldo = new_qty - qty_in_the_day
                qty = qty_in_the_day + saldo
                dic_qty_long[i] = qty
                quota_value = qty * prices_in_the_day  # verificar se é esse preço msm
                quota_value = (1 + returns.loc[i]) * quota_value
                dic_quota_value_long[i] = quota_value
                dic_saldo_long[i] = saldo
                print(aum_in_the_day)

                k += 1


            else:
                quota_value = (1 + returns.loc[i]) * quota_value
                dic_quota_value_long[i] = quota_value
                dic_qty_long[i] = qty
                print(i)

        # Short
        short_ini_period = s_wgt.groupby(pd.DatetimeIndex(s_wgt.index).to_period(rebal_freq)).nth(0)
        short_ini_period.index = s_wgt.groupby(pd.DatetimeIndex(s_wgt.index).to_period(rebal_freq)).head(1).index

        qty = (short_ini_period.iloc[1] * initial_ammount / prices.loc[short_ini_period.index[1]])
        quota_value = (short_ini_period.iloc[1] * initial_ammount / prices.loc[short_ini_period.index[1]]) * prices.loc[
            short_ini_period.index[1]]

        dic_qty_short = {}
        dic_quota_value_short = {}
        dic_saldo_short = {}

        dic_qty_short[long_ini_period.index[1]] = qty
        dic_quota_value_short[short_ini_period.index[1]] = quota_value
        dic_saldo_short[short_ini_period.index[1]] = qty

        list_rebal_dates = short_ini_period.loc[
            short_ini_period.index[short_ini_period.index > quota_value.name][0:]].index

        k = 0
        for i in returns.index[returns.index > quota_value.name]:

            if k < len(list_rebal_dates) and i == list_rebal_dates[k]:
                print(str(i) + ' hora de rebalancear')
                list_prices = prices.index.to_list()
                position = list_prices.index(list_rebal_dates[k])
                position_yesterday = position - 1
                prices_in_the_day = prices.iloc[position_yesterday]
                qty_in_the_day = dic_qty_short[list(dic_qty_short.keys())[-1]]
                aum_in_the_day = (qty_in_the_day * prices_in_the_day)
                new_pos = short_ini_period.iloc[k]
                wgt_in_the_day = aum_in_the_day / aum_in_the_day.sum()
                new_wgt = short_ini_period.iloc[k + 2]
                aum_in_the_day = aum_in_the_day.sum()
                new_qty = new_wgt * aum_in_the_day / prices_in_the_day
                new_qty[np.isnan(new_qty)] = 0
                qty_in_the_day[np.isnan(qty_in_the_day)] = 0
                saldo = new_qty - qty_in_the_day
                qty = qty_in_the_day + saldo
                dic_qty_short[i] = qty
                quota_value = qty * prices_in_the_day  # verificar se é esse preço msm
                quota_value = (1 + returns.loc[i]) * quota_value
                dic_quota_value_short[i] = quota_value
                dic_saldo_short[i] = saldo
                print(aum_in_the_day)

                k += 1


            else:
                quota_value = (1 + returns.loc[i]) * quota_value
                dic_quota_value_short[i] = quota_value
                dic_qty_short[i] = qty
                print(i)

        df_quota_long = pd.DataFrame(pd.concat(dic_quota_value_long, axis=0)).reset_index()
        df_quota_long.rename(columns={'level_0': 'date', 0: 'quota'}, inplace=True)
        df_quota_long = df_quota_long.pivot(index='date', columns='ticker', values='quota')
        df_quota_long['total_aum'] = df_quota_long.sum(axis=1)

        df_saldo_long = pd.DataFrame(pd.concat(dic_saldo_long, axis=0)).reset_index()
        df_saldo_long.rename(columns={'level_0': 'date', 0: 'qty'}, inplace=True)
        df_saldo_long = df_saldo_long.pivot(index='date', columns='ticker', values='qty')
        df_saldo_long['total_qty'] = df_saldo_long.sum(axis=1)

        df_quota_short = pd.DataFrame(pd.concat(dic_quota_value_short, axis=0)).reset_index()
        df_quota_short.rename(columns={'level_0': 'date', 0: 'quota'}, inplace=True)
        df_quota_short = df_quota_short.pivot(index='date', columns='ticker', values='quota')
        df_quota_short['total_aum'] = df_quota_short.sum(axis=1)

        df_saldo_short = pd.DataFrame(pd.concat(dic_saldo_short, axis=0)).reset_index()
        df_saldo_short.rename(columns={'level_0': 'date', 0: 'qty'}, inplace=True)
        df_saldo_short = df_saldo_short.pivot(index='date', columns='ticker', values='qty')
        df_saldo_short['total_qty'] = df_saldo_short.sum(axis=1)

        return (df_quota_long, df_saldo_long, df_quota_short, df_saldo_short)