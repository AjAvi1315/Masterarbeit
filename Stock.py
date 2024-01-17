import numericalMethods as nM
import numpy as np

from BasicValue import BasicValue
"""
The child class of BasicValue contains the functions for structuring the procedures.
The specific calculations for stocks are summarised here 
"""

class Stock(BasicValue):
    def __init__(self, start_value, sigma, mue):
        super().__init__(start_value, sigma)
        self.mue = mue

    """function for the monte-carlo-method for the individual calculation of a value"""
    def calc_mc_step(self, x, time_steps, i, z):
        h = time_steps[i] - time_steps[i - 1]
        x_t = self.mue * h + self.sigma * (h ** 0.5) * z
        x_next = x * np.exp(x_t)
        return x_next

    """function for the monte-carlo-method from numericalMethods"""
    def monte_carlo_simulation(self, time_steps, paths):
        stock_paths = nM.basic_monte_carlo(self.start_value, time_steps, paths, self.calc_mc_step)
        return stock_paths

    """calculation of cash flow as the difference between simulation paths and strike"""
    def calc_cash_flow(self, sim_matrix, strike):
        cash_flows = strike - sim_matrix
        return cash_flows

    """returns the discount values for each time step"""
    def get_discount_values(self, exercise_dates):
        discounts = []
        for date in exercise_dates:
            d_next = np.exp(-self.mue * date)
            discounts.append(d_next)
        return discounts
