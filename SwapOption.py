from Instrument import Instrument
from Option import Option
from Swap import Swap

from InterestRate import InterestRate

"""Class for managing the different procedures for options on swaps"""

class SwapOption(Instrument):
    def __init__(self, sigma, time_stamps, exercise_dates, tenor, strike, option_type, mean_reversion, forward_rates):
        interest_rate = InterestRate(0, sigma, mean_reversion)
        self.swap = Swap(tenor, interest_rate, strike, option_type, forward_rates)
        self.option = Option(time_stamps, self.swap, strike, option_type, exercise_dates)

    def pricer_monte_carlo(self, paths):
        short_rates = self.swap.underlying.monte_carlo_simulation(self.option.run_time, paths)
        discounted_values = self.swap.underlying.get_discount_values(short_rates, self.option.run_time)
        discounted_values = self.option.get_exercise_values(discounted_values)
        underlying_swap = self.option.get_underlying_cash(short_rates, discounted_values)
        coefficients = self.swap.get_coefficients(underlying_swap, discounted_values)
        opt_cash_flow = self.option.get_opt_stops(underlying_swap, coefficients)
        V = self.option.get_fair_value(opt_cash_flow)
        return V
