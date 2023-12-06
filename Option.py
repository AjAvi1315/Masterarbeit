import numericalMethods


class Option:
    def __init__(self, run_time, exercise_dates, underlyning, strike, option_type):
        self.run_time = run_time
        self.exercise_dates = exercise_dates
        self.underlyning = underlyning
        self.strike = strike
        self.option_type = option_type

    def approximate_underlyning_MC(self, pfade):
        S = self.underlyning.monte_carlo_simulation(pfade)
        return S

    def monte_carlo_simulation(self, path):
        mc = numericalMethods.BasicMonteCarlo(self.underlyning)
        mc.test()

