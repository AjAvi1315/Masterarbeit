from StockOption import StockOption
import numpy as np

def stockoption_test():
# input parameter Aktien
    s0 = 98
    step = 1 / 12  # Anzahl zu generierende Monate
    t = np.array(range(1, 37))
    T = t * step
    mue = 0.01
    sigma = 0.2
    pfade = 1000
    t_pay = [0, 11, 23, 35]
    strike = 50
    option_type = 1

    stock_option = StockOption(s0, mue, sigma, T, t_pay, strike, option_type)
    S = stock_option.pricer_monte_carlo(pfade)
    #print(len(S))