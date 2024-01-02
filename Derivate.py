class Derivate:
    def __init__(self, run_time, underlyning, strike, type):
        self.run_time = run_time
        self.underlyning = underlyning
        self.strike = strike
        self.type = type

    """
    calculates the cash flow at several points in time
    """
    def get_cash_flow(self, sim_matrix, exercise_dates=None):
        raise NotImplementedError("Funktion get_cash_flow needs to be implemented")

    """
    Returns the fair value of the derivative as an average at several points in time
    """
    def get_fair_value(self, cash_flow_matrix):
        raise NotImplementedError("Funktion get_fair_value needs to be implemented")
