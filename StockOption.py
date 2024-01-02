from Option import Option
from Stock import Stock


class StockOption:

    def __init__(self, start_value, mue, sigma, time_stamps, exercise_dates, strike, option_type):
        stock = Stock(start_value, mue, sigma)
        self.option = Option(time_stamps, exercise_dates, stock, strike, option_type)

    def pricer_monte_carlo(self, paths):
        print("Do some Pricing")
        S = self.option.underlyning.monte_carlo_simulation(self.option.run_time, paths)
        S_exercise = self.option.get_exercise_underlyning(S)
        #print(S)
        cash_flows = self.option.get_cash_flow(S_exercise)
        print('__________')
        #print(len(cash_flows[0]))
        #print(cash_flows)
        opt_cash_flow = self.option.get_opt_stops(S_exercise, cash_flows)
        #print(opt_cash_flow)
        V = self.option.get_fair_value(opt_cash_flow)
        print(V)
        return V
