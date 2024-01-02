import numericalMethods as nM
import numpy as np
import math as math

from BasicValue import BasicValue


class InterestRate(BasicValue):
    def __init__(self, start_value, sigma, a):
        super().__init__(start_value, sigma)
        self.a = a

    def calc_mc_step(self, x, time_steps, i, z):
        return self.calc_step_hjm_hw(x, time_steps, i, z)

    def calc_step_hjm_hw(self, x, time_steps, i, z):
        g = math.exp(-self.a * (time_steps[i] - time_steps[i - 1]))
        G = (1 - g) / self.a
        mue = g * (x + G * y[i - 1])
        sig = y[i] - g ** 2 * y[i - 1]
        x_next = mue + math.sqrt(sig) * z
        return x_next

    def pre_calc_hjm_hw(self, time_steps):
        global sigma_time
        global y
        sigma_time = [self.sigma]
        y = [0]
        for k in range(1, len(time_steps)):
            s = self.sigma * ((1 - np.exp(-self.a * (time_steps[k] - time_steps[k - 1]))) / self.a)
            sigma_time.append(s)

        for k in range(2, len(time_steps)):
            y_next = 0
            for j in range(1, k):
                h1 = time_steps[k] - time_steps[j]
                h2 = time_steps[k] - time_steps[j - 1]
                p = np.exp(-2 * self.a * h1) - np.exp(-2 * self.a * h2)
                q = (sigma_time[j] ** 2) / (2 * self.a)
                y_next = y_next + (p * q)
            y.append(y_next)

    def monte_carlo_simulation(self, time_steps, paths):
        self.pre_calc_hjm_hw(time_steps)
        short_rates = nM.basic_monte_carlo(self.start_value, time_steps, paths, self.calc_mc_step)
        return short_rates

    # calculate the bank accounts
    def get_discount_values(self, sim_matrix, times):
        print('calc bank account')
        discount_values = []
        for x in sim_matrix:
            b = [1]
            for k in range(1, len(times) - 1):
                g = math.exp(-self.a * (times[k] - times[k - 1]))
                G = (1 - g) / self.a
                p = (math.exp(-x[k] * times[k]) / math.exp(-x[k - 1] * times[k - 1])) * math.exp(
                    -G * x[k - 1] - ((G ** 2) / 2 * y[k - 1]))
                b_next = b[k - 1] / p
                b.append(b_next)
            discount_values.append(b)
        return np.array(discount_values)

    """
        clac the underlyning cash flow for the swap in definition time
    """

    def calc_cash_flow(self, run_time, i_ex_time, strike, r, x):
        print('calc cash_flow interest rate')
        # print(run_time)
        # print(i_ex_time)
        # print(strike)
        # print(r)
        # print(x)

        p_fixed = 0
        for i in range(i_ex_time, len(run_time) - 2):
            g = math.exp(-self.a * (run_time[i] - run_time[i_ex_time]))
            G = (1 - g) / self.a
            p_fixed += strike * (math.exp(-r[i] * run_time[i]) / math.exp(-r[i_ex_time] * run_time[i_ex_time])) * math.exp(-G * x - ((G ** 2) / 2 * y[i_ex_time]))

        p_float = 0
        # erster wert wird entfernt P(T_E,T_j) für T_E=T_j
        for i in range(i_ex_time + 1, len(run_time) - 2):
            g = math.exp(-self.a * (run_time[i] - run_time[i_ex_time]))
            G = (1 - g) / self.a
            p_float += (strike - 1) * ((math.exp(-r[i] * run_time[i]) / math.exp(-r[i_ex_time] * run_time[i_ex_time])) * math.exp(-G * x - ((G ** 2) / 2 * y[i_ex_time])))

        # Summiere bonds zur foated rate und annahme D = c-1
        p_k = (math.exp(-r[i_ex_time] * run_time[i_ex_time]) / math.exp(-r[i_ex_time] * run_time[i_ex_time]))
        G = (1 - math.exp(-self.a * (run_time[len(run_time) - 2] - run_time[i_ex_time]))) / self.a
        p_n = math.exp(-r[len(run_time) - 2] * run_time[len(run_time) - 2]) / math.exp(-r[i_ex_time] * run_time[i_ex_time]) * math.exp(-G * x - ((G ** 2) / 2 * y[i_ex_time]))
        zb = -p_k + p_fixed - p_float + p_n

        return zb
