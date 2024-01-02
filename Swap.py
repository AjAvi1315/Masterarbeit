import numericalMethods as nM
import numpy as np
import math as math
import scipy.interpolate as sInter

from Derivate import Derivate


class Swap(Derivate):
    def __init__(self, run_time, underlyning, strike, type, variable_rates):
        super().__init__(run_time, underlyning, strike, type)
        time_step = run_time[1] - run_time[0]
        self.r = self.interpolate_forward_rates(time_step, variable_rates)

    def interpolate_forward_rates(self, time_step, forward_rates):
        #time_max = forward_rates[0][-1]/time_step + 2
        #time_max = int(math.ceil(time_max))
        #t = np.array(range(0, time_max))  # jährliche Timesteps
        #f = sInter.CubicSpline(forward_rates[0], forward_rates[1])
        #x_new = t / time_step
        x = [0, 1 / 12, 3 / 12, 6 / 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
        y = [-0.586, -0.57705, -0.56835, -0.47205, -0.1697, 0.48395, 0.7855, 0.9385, 1.0275, 1.0965, 1.1605, 1.228,
             1.293, 1.353, 1.538, 1.523]
        t = np.array(range(0, 12 * 15 + 2))  # jährliche Timesteps
        f = sInter.CubicSpline(x, y)
        x_new = t * (1 / 12)
        y_new = f(x_new)
        return y_new / 100

    """
    calculate bankaccounts and swap underlynings for option
    for example calculate only interest rate swap
    """
    def get_cash_flow(self, sim_matrix, exercise_dates=None):
        cash_flow = []
        if exercise_dates is None:
            cash_flow = self.underlyning.calc_cash_flow(sim_matrix, self.strike, self.run_time)
        else:
            for j in range(0, len(sim_matrix)):
                # speicherung der Werte des zu betrachtenden Pfad
                x = sim_matrix[j]
                u = []
                # Durchlaufe alle Ausübungszeitpunkte des Pfades
                for k, t_ex in enumerate(exercise_dates):
                    k_ex = np.where(self.run_time == t_ex)[0][0]
                    # Summiere Zerosbons zur fixed rate
                    cash = self.type * self.underlyning.calc_cash_flow(self.run_time, k_ex, self.strike, self.r, x[k_ex])
                    u.append(cash)
                cash_flow.append(u)
        return cash_flow

    def get_coefficients(self, bonds, bank_accounts):
        H = np.zeros((len(bank_accounts), len(bank_accounts[0])))
        for j in range(0, len(bonds)):
            for i in range(len(bank_accounts[0]) - 2, -1, -1):
                v = 0
                if bonds[j][i + 1] >= H[j][i + 1]:
                    v = bonds[j][i + 1]
                else:
                    v = H[j][i + 1]
                H[j][i] = bank_accounts[j][i] * (v / bank_accounts[j][i + 1])
        coeffizents = bonds - H
        coeffizents[coeffizents < 0.0] = 0.0
        return coeffizents
