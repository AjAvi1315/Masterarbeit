import numpy as np
import numericalMethods as nM
from Derivatives import Derivatives

"""
The child class of derivatives contains the functions for structuring the procedures.
In particular, all those used for options are recorded here.
"""

class Option(Derivatives):
    def __init__(self, run_time, underlying, strike, type, exercise_dates):
        super().__init__(run_time, underlying, strike, type)
        self.exercise_dates = exercise_dates

    """get the approximate values from the underlying to exercises dates"""
    def get_exercise_values(self, sim_matrix):
        u_exercise = np.zeros((len(sim_matrix), np.size(self.exercise_dates)))
        j = []
        for t in self.exercise_dates:
            j.append(np.where(self.run_time == t)[0][0])
        for i, sim_col in enumerate(sim_matrix):
            u_exercise[i] = sim_col[j]
        return u_exercise

    """Returns the discounted cash flow of the option to the underlying asset"""
    def get_cash_flow(self, sim_matrix, exercise_dates=None):
        cash_flows = self.type * self.underlying.calc_cash_flow(sim_matrix, self.strike)
        discount_values = self.underlying.get_discount_values(self.exercise_dates)
        for i, i_cash in enumerate(cash_flows):
            cash_flows[i] = discount_values * i_cash

        cash_flows[cash_flows < 0.0] = 0.0
        return cash_flows

    """
    needed function for calculate nested derivate
    """
    def get_underlying_cash(self, sim_matrix, discount_values):
        u_cash = self.underlying.get_cash_flow(sim_matrix, self.exercise_dates)
        underlying_cash = discount_values*self.type*u_cash
        return underlying_cash

    """
    This function is used to call the Longstaff-Schwartz method.
    A corresponding option could be added here to allow the use of other procedures.
    """
    def get_opt_stops(self, exercise_sim_values, cash_flows):
        opt_stop_cash = nM.longstaff_schwartz_method(exercise_sim_values, cash_flows)
        return opt_stop_cash

    """Calculates the fair value from a matrix with optimal exercise times"""
    def get_fair_value(self, cash_flow_matrix):
        v_0 = 0.0
        n = len(cash_flow_matrix)
        for i in range(n):
            for v in cash_flow_matrix[i]:
                if v > 0.0:
                    v_0 += v / n
                    break
        return v_0
