from StockOption import StockOption
import numpy as np

if __name__ == '__main__':
    # input parameter
    s0 = 98
    step = 1 / 12  # Anzahl zu generierende Monate
    t = np.array(range(1, 37))
    T = t * step
    mue = 0.01
    sigma = 0.2
    pfade = 1000
    t_pay = [0, 11, 23, 35]
    strike = 100
    option_type = 1

    stock_option = StockOption(s0, mue, sigma, T, t_pay, strike, option_type)
    S = stock_option.pricerMC(pfade)
    #print(len(S))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
