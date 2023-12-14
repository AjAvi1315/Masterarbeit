import numpy as np
import numericalMethods as nM


class Option:
    def __init__(self, run_time, exercise_dates, underlyning, strike, option_type):
        self.run_time = run_time
        self.exercise_dates = exercise_dates
        self.underlyning = underlyning
        self.strike = strike
        self.option_type = option_type

    # get the approximate values from the underlyning to exercises dates
    def get_exercise_underlyning(self, sim_matrix):
        u_exercise = np.zeros((len(sim_matrix), np.size(self.exercise_dates)))
        for i, sim_col in enumerate(sim_matrix):
            # print(u_exercise)
            u_exercise[i] = sim_col[self.exercise_dates]
        return u_exercise

    def get_cash_flow(self, sim_matrix):
        cash_flows = self.option_type * self.underlyning.calc_cash_flow(sim_matrix, self.strike)
        return cash_flows

    def get_opt_stops(self, exercise_sim_values, cash_flows):
        discont_values = self.underlyning.get_discont_values([0, 1, 2, 3])
        # print(discont_values)
        opt_stop_cash = nM.longstaff_schwarz_method(exercise_sim_values, cash_flows, discont_values)
        return opt_stop_cash

    def get_fair_value(self, opt_cash):
        v_0 = 0.0
        n = len(opt_cash)
        for i in range(n):
            for v in opt_cash[i]:
                v_0 += v / n
        return v_0
