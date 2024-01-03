import numericalMethods as nM
import numpy as np
import math as math
import scipy.interpolate as sInter

from Derivate import Derivate


class Swap(Derivate):
    def __init__(self, run_time, underlyning, strike, type, variable_rates):
        super().__init__(run_time, underlyning, strike, type)
        self.r = self.interpolate_forward_rates(variable_rates)

    def interpolate_forward_rates(self, forward_rates):
        f = sInter.CubicSpline(forward_rates["x"], forward_rates["y"])
        y_new = f(self.run_time)
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
