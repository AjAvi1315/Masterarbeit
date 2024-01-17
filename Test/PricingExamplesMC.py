import numpy as np

"""This file is only used for testing. It contains the input parameters and returns them."""


def stock_option_test():
    s0 = 98
    step = 1 / 12
    t = np.array(range(0, 38))
    T = t * step
    mue = 0.01
    sigma = 0.2
    t_pay = [0, 1, 2, 3]
    strike = 100
    option_type = -1
    data = {'start_value': s0, 'sigma': sigma, 'mue': mue, 'run_time': T,
            'exercises': t_pay, 'strike': strike, 'option_type': option_type}
    return data


def swap_option_test():
    variable_rates = {"x": [0, 1 / 12, 3 / 12, 6 / 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
                      "y": [-0.586, -0.57705, -0.56835, -0.47205, -0.1697, 0.48395, 0.7855,
                            0.9385, 1.0275, 1.0965, 1.1605, 1.228, 1.293, 1.353, 1.538, 1.523]}
    a = 0.03
    sigma = 0.1
    time_steps = 12
    t = np.array(range(0, time_steps * 4 + 2))
    t = t / time_steps
    t_E = np.array([1, 1.5, 2, 2.5, 3])
    c = 0.01863
    option_type = 1
    tenor = np.array(range(0, time_steps * 15 + 1))
    tenor = tenor / time_steps
    data = {'sigma': sigma, 'run_time': t, 'exercises': t_E, 'tenor': tenor, 'strike': c,
            'option_type': option_type, 'mean_reversion': a, 'forward_rates': variable_rates}
    return data
