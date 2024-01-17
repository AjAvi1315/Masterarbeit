"""Base class for all future financial instruments
   It contains the functions for the different pricer
"""
class Instrument:
    def pricer_monte_carlo(self, paths):
        raise NotImplementedError("The Monte-Carlo-pricer is not implemented for this instrument.")
