from Option import Option
from Stock import Stock
class StockOption:

    def __init__(self, start_value, mue, sigma, time_stamps, exercise_dates, strike, option_type):
        #self.stock = Stock(start_value, mue, sigma)
        self.stock = 1
        self.option = Option(time_stamps, exercise_dates, self.stock, strike, option_type)


    def pricerMC(self, paths):
        print("Do some Pricing")
        S = self.option.monte_carlo_simulation(paths)

