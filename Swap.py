import numpy as np
import scipy.interpolate as sInter

from Derivatives import Derivatives

"""
The child class of derivatives contains the functions for structuring the procedures.
In particular, all those used for swaps are recorded here.
"""


class Swap(Derivatives):
    def __init__(self, run_time, underlying, strike, type, variable_rates):
        super().__init__(run_time, underlying, strike, type)
        self.r = self.interpolate_forward_rates(variable_rates)

    """function for interpolating the given yield curve"""
    def interpolate_forward_rates(self, forward_rates):
        f = sInter.CubicSpline(forward_rates["x"], forward_rates["y"])
        y_new = f(self.run_time)
        return y_new / 100

    """
    calculate bankaccounts and swap underlyings for option
    for example calculate only interest rate swap
    """

    def get_cash_flow(self, sim_matrix, exercise_dates=None):
        cash_flow = []
        if exercise_dates is None:
            cash_flow = self.underlying.calc_cash_flow(sim_matrix, self.strike, self.run_time)
        else:
            for j in range(0, len(sim_matrix)):
                x = sim_matrix[j]
                u = []
                for k, t_ex in enumerate(exercise_dates):
                    k_ex = np.where(self.run_time == t_ex)[0][0]
                    cash = self.type * self.underlying.calc_cash_flow(self.run_time, k_ex, self.strike, self.r, x[k_ex])
                    u.append(cash)
                cash_flow.append(u)
        return cash_flow
    """
    functions calculate the conditional continuation values for the regression
    It is possible that a different solution will have to be found if additional pricers are added
    """
    def get_coefficients(self, bonds, bank_accounts):
        H = np.zeros((len(bank_accounts), len(bank_accounts[0])))
        for j in range(0, len(bonds)):
            for i in range(len(bank_accounts[0]) - 2, -1, -1):
                if bonds[j][i + 1] >= H[j][i + 1]:
                    v = bonds[j][i + 1]
                else:
                    v = H[j][i + 1]
                H[j][i] = bank_accounts[j][i] * (v / bank_accounts[j][i + 1])
        coefficients = bonds - H
        coefficients[coefficients < 0.0] = 0.0
        return coefficients
