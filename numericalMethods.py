import numpy as np




class NumericalMethods:
    def __init__(self, finance_object):
        self.finance_object = finance_object

class BasicMonteCarlo(NumericalMethods):
    def __init__(self, finance_object):
        super().__init__(finance_object)
        # check if finance objekt has interface


    def calc_mue(self, i, param):
        raise NotImplementedError

    def calc_sigma(self, i, param):
        raise NotImplementedError

    def get_start_value(self):
        raise NotImplementedError

    def get_run_time_size(self):
        raise NotImplementedError

    def get_paths(self):
        raise NotImplementedError

    def calculate(self):
        S = np.array([])
        for j in range(37):
            Z = np.random.normal(loc=0, scale=1, size=self.get_run_time_size())
            s_j = np.array([self.get_start_value()])

            for i in range(1, self.get_run_time_size()):
                x_t = self.calc_mue(i, s_j[i - 1]) + self.calc_sigma(i, i - 1) * Z[i]
                next_s = s_j[i - 1] * np.exp(x_t)
                s_j = np.append(s_j, next_s)

            S = np.append(S, s_j)
        return S

