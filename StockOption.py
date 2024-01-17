from Instrument import Instrument
from Option import Option
from Stock import Stock

"""Class for managing the different procedures for options on stocks"""
class StockOption(Instrument):

    def __init__(self, start_value, sigma, mue, time_stamps, exercise_dates, strike, option_type):
        stock = Stock(start_value, sigma, mue)
        self.option = Option(time_stamps, stock, strike, option_type, exercise_dates)

    def pricer_monte_carlo(self, paths):
        S = self.option.underlying.monte_carlo_simulation(self.option.run_time, paths)
        S_exercise = self.option.get_exercise_values(S)
        cash_flows = self.option.get_cash_flow(S_exercise)
        opt_cash_flow = self.option.get_opt_stops(S_exercise, cash_flows)
        V = self.option.get_fair_value(opt_cash_flow)
        return V
