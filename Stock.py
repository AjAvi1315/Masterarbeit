import numericalMethods as nM
import numpy as np

class Stock:
    def __init__(self, start_value, mue, sigma):
        self.start_value = start_value
        self.mue = mue
        self.sigma = sigma

    ######################################################
    ###  Individual functions for Monte-Carlo-Pricing  ###
    ######################################################
    def calc_mc_step(self, x, h, z):
        x_t = self.mue * h + self.sigma * h ** 0.5 * z
        x_next = x * np.exp(x_t)
        return x_next

    def monte_carlo_simulation(self, time_steps, paths):
        stock_paths = nM.basic_monte_carlo(self.start_value, time_steps, paths, self.calc_mc_step)
        return stock_paths

    def calc_cash_flow(self, sim_matrix, strike):
        cash_flows = sim_matrix - strike
        return cash_flows

    def get_discont_values(self, exercise_dates):
        disconts = []
        for date in exercise_dates:
            d_next = np.exp(-self.mue*date)
            disconts.append(d_next)
        return disconts
