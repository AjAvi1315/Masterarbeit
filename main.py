from InstrumentInitializer import InstrumentInitializer
from SwapOption import SwapOption

import numpy as np

if __name__ == '__main__':
    # input parameter Swap
    x = np.array([[0, 1 / 12, 3 / 12, 6 / 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]])
    y = np.array(
        [[-0.586, -0.57705, -0.56835, -0.47205, -0.1697, 0.48395, 0.7855, 0.9385, 1.0275, 1.0965, 1.1605, 1.228, 1.293,
          1.353, 1.538, 1.523]])

    # forward_rates = np.concatenate((x, y), axis=0)
    variable_rates = {"x": [0, 1 / 12, 3 / 12, 6 / 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
                      "y": [-0.586, -0.57705, -0.56835, -0.47205, -0.1697, 0.48395, 0.7855, 0.9385, 1.0275, 1.0965,
                            1.1605, 1.228, 1.293,
                            1.353, 1.538, 1.523]}

    a = 0.03  # mean reserve
    sigma = 0.1  # ausgangs Sigma dies sollte vorab in einer Kaliebrierung angenähert werden
    r_float = 0.03  # es ist Möglich auch eine kostante Zinsen für P(0,t) zu verwenden
    time_steps = 12
    t = np.array(range(0,
                       time_steps * 4 + 2))  # jährliche Timesteps || +2 für bessere Schleifen duchläufe um auf exat 15 zu kommen
    t = t / time_steps
    t_len = len(t)
    t_E = np.array([1, 1.5, 2, 2.5, 3])  # Ausübungszeitpunkte || ist bei den H auf genau 5 abgestimmt
    c = 0.01863  # strike aus exel Datei
    paths = 10  # Anzahl zu Simulierende Pfade
    mue = 0
    option_type = 1
    tenor = np.array(range(0, time_steps * 15 + 1))
    tenor = tenor / time_steps
    data = {'sigma': sigma, 'run_time': t, 'exercises': t_E, 'tenor': tenor, 'strike':c, 'option_type': option_type, 'mean_reversion': a, 'forward_rates': variable_rates }
    #swap_option = SwapOption(sigma, t, t_E, tenor, c, option_type, a, variable_rates)
    #swap_option.pricer_monte_carlo(paths)

    instrument = InstrumentInitializer("SwapOption", data)
    test = instrument.initialize()
    test.pricer_monte_carlo(paths)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
