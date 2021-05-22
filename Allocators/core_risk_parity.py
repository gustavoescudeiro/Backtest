import pandas as pd
import numpy as np
import datetime
from scipy.optimize import minimize
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
    # covariances = 52.0 * \
    # prices.asfreq('W-FRI').pct_change().iloc[1:, :].cov().values

    # We calculate the covariance matrix
    covariances = 252.0 * \
                  prices.pct_change().iloc[1:, :].cov().values

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
            df_long = df_sub[long_position[df_sub.index[len(df_sub.index)-1]]]
            d_long = get_weight(df_long)
            dic_long[df_long.index[-1]] = d_long

        df_long = pd.concat(dic_long, axis=0)
        df_long = pd.DataFrame(df_long).reset_index()
        df_long.rename(columns={'level_0': 'date'}, inplace=True)
        df_long = df_long.pivot(index='date', columns='ticker', values='weight')

    return(df_long)