import numericalMethods as nM
import numpy as np

from BasicValue import BasicValue


class Stock(BasicValue):
    def __init__(self, start_value, mue, sigma):
        super().__init__(start_value, sigma)
        self.mue = mue


    ######################################################
    ###  Individual functions for Monte-Carlo-Pricing  ###
    ######################################################
    def calc_mc_step(self, x, time_steps, i, z):
        h = time_steps[i] - time_steps[i - 1]
        x_t = self.mue * h + self.sigma * (h ** 0.5) * z
        x_next = x * np.exp(x_t)
        return x_next

    def monte_carlo_simulation(self, time_steps, paths):
        stock_paths = nM.basic_monte_carlo(self.start_value, time_steps, paths, self.calc_mc_step)
        return stock_paths

    def calc_cash_flow(self, sim_matrix, strike):
        cash_flows = sim_matrix - strike
        return cash_flows

    def get_discount_values(self, exercise_dates):
        discounts = []
        for date in exercise_dates:
            d_next = np.exp(-self.mue*date)
            discounts.append(d_next)
        return discounts
