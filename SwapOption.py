from Instrument import Instrument
from Option import Option
from Swap import Swap

from InterestRate import InterestRate

import numpy as np
import math as math


class SwapOption(Instrument):
    def __init__(self, sigma, time_stamps, exercise_dates, tenor, strike, option_type, mean_reversion, forward_rates):
        interest_rate = InterestRate(0, sigma, mean_reversion)
        self.swap = Swap(tenor, interest_rate, strike, option_type, forward_rates)
        self.option = Option(time_stamps, self.swap, strike, option_type, exercise_dates)

    # interpolate given forward rates of swap for all needed timestamps

    def pricer_monte_carlo(self, paths):
        print("Do Swap Pricing")
        short_rates = self.swap.underlyning.monte_carlo_simulation(self.option.run_time, paths)
        discounted_values = self.swap.underlyning.get_discount_values(short_rates, self.option.run_time)
        discounted_values = self.option.get_exercise_underlyning(discounted_values)
        underlynings = self.option.get_underlyning_cash(short_rates, discounted_values)
        coeffizents = self.swap.get_coefficients(underlynings, discounted_values)
        opt_cash_flow = self.option.get_opt_stops(underlynings, coeffizents)
        print(opt_cash_flow)
        #print(len(short_rates))
