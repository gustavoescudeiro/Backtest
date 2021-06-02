import pandas as pd
import numpy as np
import datetime
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf


TOLERANCE = 1e-10
def _allocation_risk(weights, covariances):

    # We calculate the risk of the weights distribution
    portfolio_risk = np.sqrt((weights * covariances * weights.T))[0, 0]

    # It returns the risk of the weights distribution
    return portfolio_risk


def _assets_risk_contribution_to_allocation_risk(weights, covariances):

    # We calculate the risk of the weights distribution
    portfolio_risk = _allocation_risk(weights, covariances)

    # We calculate the contribution of each asset to the risk of the weights
    # distribution
    assets_risk_contribution = np.multiply(weights.T, covariances * weights.T) \
        / portfolio_risk

    # It returns the contribution of each asset to the risk of the weights
    # distribution
    return assets_risk_contribution


def _risk_budget_objective_error(weights, args):

    # The covariance matrix occupies the first position in the variable
    covariances = args[0]

    # The desired contribution of each asset to the portfolio risk occupies the
    # second position
    assets_risk_budget = args[1]

    # We convert the weights to a matrix
    weights = np.matrix(weights)

    # We calculate the risk of the weights distribution
    portfolio_risk = _allocation_risk(weights, covariances)

    # We calculate the contribution of each asset to the risk of the weights
    # distribution
    assets_risk_contribution = \
        _assets_risk_contribution_to_allocation_risk(weights, covariances)

    # We calculate the desired contribution of each asset to the risk of the
    # weights distribution
    assets_risk_target = \
        np.asmatrix(np.multiply(portfolio_risk, assets_risk_budget))

    # Error between the desired contribution and the calculated contribution of
    # each asset
    error = \
        sum(np.square(assets_risk_contribution - assets_risk_target.T))[0, 0]

    # It returns the calculated error
    return error


def _get_risk_parity_weights(covariances, assets_risk_budget, initial_weights):

    # Restrictions to consider in the optimisation: only long positions whose
    # sum equals 100%
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0},
                   {'type': 'ineq', 'fun': lambda x: x})

    # Optimisation process in scipy
    optimize_result = minimize(fun=_risk_budget_objective_error,
                               x0=initial_weights,
                               args=[covariances, assets_risk_budget],
                               method='SLSQP',
                               constraints=constraints,
                               tol=TOLERANCE,
                               options={'disp': False})

    # Recover the weights from the optimised object
    weights = optimize_result.x

    # It returns the optimised weights
    return weights


def get_weight(df=None):
    prices = df.copy()
    # We download the prices from Yahoo Finance
    # prices = df.iloc[:,:].asfreq('B').ffill() @TODO esse metodo esta adicionando mais linhas

    # We calculate the covariance matrix
    #covariances = 52.0 * \
    #prices.asfreq('W-FRI').pct_change().iloc[1:, :].cov().values

    # We calculate the covariance matrix
    #covariances = 252.0 * \
    #             prices.pct_change().iloc[1:, :].cov().values

    # We calculate the covariance matrix
    prices = prices.loc[:, (prices == 0).mean() < .1]
    cov = LedoitWolf().fit(prices.pct_change().dropna().values * 252)
    covariances = cov.covariance_


    # The desired contribution of each asset to the portfolio risk: we want all
    # asset to contribute equally
    assets_risk_budget = [1 / prices.shape[1]] * prices.shape[1]

    # Initial weights: equally weighted
    init_weights = [1 / prices.shape[1]] * prices.shape[1]

    # Optimisation process of weights
    weights = \
        _get_risk_parity_weights(covariances, assets_risk_budget, init_weights)

    # Convert the weights to a pandas Series
    weights = pd.Series(weights, index=prices.columns, name='weight')

    # It returns the optimised weights
    return weights


def get_weights_rp(signal = None, prices = None, long_and_short = False, window = 222, freq = 'M'):
    w = window



    ini_period = signal.groupby(pd.DatetimeIndex(signal.index).to_period(freq)).nth(0)
    ini_period.index = signal.groupby(pd.DatetimeIndex(signal.index).to_period(freq)).head(1).index


    if long_and_short == False:
        long_position = {}
        for i in signal.index:
            all_positions = signal.loc[i, :]
            lp = all_positions[all_positions == 1].index.to_list()
            long_position[i] = lp

        dic_long = {}
        for i in ini_period.index[::-1]:
            #first_date = prices.index[0] + pd.Timedelta(days=w)
            #df_sub = prices[prices.index >= first_date]
            init_date = i - pd.Timedelta(days=w)
            df_sub = prices[(prices.index >= init_date) & (prices.index <= i)]
            if df_sub.shape[0] >= int(0.65*w):

                df_long = df_sub[long_position[df_sub.index[len(df_sub.index)-1]]]
                df_long = df_long.dropna(axis=1)
                d_long = get_weight(df_long)
                print(d_long, i)
                dic_long[df_long.index[-1]] = d_long


                df_long = pd.concat(dic_long, axis=0)
                df_long = pd.DataFrame(df_long).reset_index()
                df_long.rename(columns={'level_0': 'date'}, inplace=True)
                df_long = df_long.pivot(index='date', columns='ticker', values='weight')
                df_long['date_sort'] = df_long.index
                df_long = df_long.sort_values(['date_sort'], ascending = True)
                df_long.drop(['date_sort'], axis=1, inplace=True)

        return(df_long)
    else:
        long_position = {}
        for i in signal.index:
            all_positions = signal.loc[i, :]
            lp = all_positions[all_positions == 1].index.to_list()
            long_position[i] = lp

        dic_long = {}
        for i in ini_period.index[::-1]:
            # first_date = prices.index[0] + pd.Timedelta(days=w)
            # df_sub = prices[prices.index >= first_date]
            init_date = i - pd.Timedelta(days=w)
            df_sub = prices[(prices.index >= init_date) & (prices.index <= i)]
            if df_sub.shape[0] >= int(0.65 * w):
                df_long = df_sub[long_position[df_sub.index[len(df_sub.index) - 1]]]
                df_long = df_long.dropna(axis=1)
                d_long = get_weight(df_long)
                print(d_long, i)
                dic_long[df_long.index[-1]] = d_long

                df_long = pd.concat(dic_long, axis=0)
                df_long = pd.DataFrame(df_long).reset_index()
                df_long.rename(columns={'level_0': 'date'}, inplace=True)
                df_long = df_long.pivot(index='date', columns='ticker', values='weight')
                df_long['date_sort'] = df_long.index
                df_long = df_long.sort_values(['date_sort'], ascending=True)
                df_long.drop(['date_sort'], axis=1, inplace=True)

        dic_short = {}
        for i in ini_period.index[::-1]:
            # first_date = prices.index[0] + pd.Timedelta(days=w)
            # df_sub = prices[prices.index >= first_date]
            init_date = i - pd.Timedelta(days=w)
            df_sub = prices[(prices.index >= init_date) & (prices.index <= i)]
            if df_sub.shape[0] >= int(0.65 * w):
                df_short = df_sub[short_position[df_sub.index[len(df_sub.index) - 1]]]
                df_short = df_short.dropna(axis=1)
                d_short = get_weight(df_short)
                print(d_short, i)
                dic_short[df_short.index[-1]] = d_short

                df_short = pd.concat(dic_short, axis=0)
                df_short = pd.DataFrame(df_short).reset_index()
                df_short.rename(columns={'level_0': 'date'}, inplace=True)
                df_short = df_short.pivot(index='date', columns='ticker', values='weight')
                df_short['date_sort'] = df_short.index
                df_short = df_short.sort_values(['date_sort'], ascending=True)
                df_short.drop(['date_sort'], axis=1, inplace=True)

        return(df_long, df_short)






