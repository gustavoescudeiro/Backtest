import pandas as pd


def get_weights(df, long_and_short=False):
    if long_and_short == False:
        lp = df[df == 1]
        lp['sum'] = lp.sum(axis=1)
        lp = lp.div(lp['sum'], axis=0)
        lp.drop(['sum'], axis=1, inplace=True)
        return (lp)




    else:
        lp = df[df == 1]
        sp = df[df == -1]

        lp['sum'] = lp.sum(axis=1)
        sp['sum'] = sp.sum(axis=1)

        lp = lp.div(lp['sum'], axis=0)
        sp = sp.div(sp['sum'], axis=0)

        lp.drop(['sum'], axis=1, inplace=True)
        sp.drop(['sum'], axis=1, inplace=True)
        return (lp, sp)