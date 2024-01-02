
class BasicValue:

    def __init__(self, start_value, sigma):
        self.start_value = start_value
        self.sigma = sigma


    """needed Funktions for Monte Carlo Simulation"""
    def monte_carlo_simulation(self, time_steps, paths):
        raise NotImplementedError("Funktion monte_carlo_simulation needs to be implemented")
    
    def calc_mc_step(self, x, time_steps, i, z):
        raise NotImplementedError("Funktion calc_mc_step needs to be implemented")