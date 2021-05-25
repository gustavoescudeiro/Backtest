from Allocators.get_one_over_n_weights import *
from Allocators.core_risk_parity import *

def generate_weights(**kwargs, model = '1/n'):
    if model == '1/n':
        return get_weights(kwargs['df'], kwargs['long_and_short'])

    elif model == 'risk_parity':
        return get_weights_rp(kwargs['signal'], kwargs['prices'], kwargs['long_and_short'], kwargs['window'])


