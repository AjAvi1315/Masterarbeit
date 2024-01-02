import numpy as np
import numericalMethods as nM
from Derivate import Derivate


class Option(Derivate):
    def __init__(self, run_time, underlyning, strike, type, exercise_dates):
        super().__init__(run_time, underlyning, strike, type)
        self.exercise_dates = exercise_dates

    # get the approximate values from the underlyning to exercises dates
    def get_exercise_underlyning(self, sim_matrix):
        u_exercise = np.zeros((len(sim_matrix), np.size(self.exercise_dates)))
        j = []
        for t in self.exercise_dates:
            j.append(np.where(self.run_time == t)[0][0])
        for i, sim_col in enumerate(sim_matrix):
            # print(u_exercise)self.exercise_dates
            u_exercise[i] = sim_col[j]
        return u_exercise

    def get_cash_flow(self, sim_matrix, exercise_dates=None):
        cash_flows = self.type * self.underlyning.calc_cash_flow(sim_matrix, self.strike)
        return cash_flows

    """
    needed function for calculate nested derivate
    """
    def get_underlyning_cash(self, sim_matrix, discount_values):
        u_cash = self.underlyning.get_cash_flow(sim_matrix, self.exercise_dates)
        underlyning_cash = discount_values*self.type*u_cash
        print(underlyning_cash)
        return underlyning_cash

    def get_opt_stops(self, exercise_sim_values, cash_flows):
        #discount_values = self.underlyning.get_discount_values([0, 1, 2, 3])
       # opt_stop_cash = nM.longstaff_schwarz_method(exercise_sim_values, cash_flows, discount_values)
        # print(discont_values)
        opt_stop_cash = nM.longstaff_schwarz_method(exercise_sim_values, cash_flows)
        return opt_stop_cash

    def get_fair_value(self, cash_flow_matrix):
        v_0 = 0.0
        n = len(cash_flow_matrix)
        for i in range(n):
            for v in cash_flow_matrix[i]:
                v_0 += v / n
        return v_0
