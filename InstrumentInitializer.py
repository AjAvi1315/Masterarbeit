from StockOption import StockOption
from SwapOption import SwapOption

"""Factory class for the different financial instruments"""


class InstrumentInitializer:
    def __init__(self, instrument_type, data):
        self.instrument_type = instrument_type
        self.data = data

    def initialize(self):
        if self.instrument_type == 'SwapOption':
            return self.initialize_swaption()
        elif self.instrument_type == 'StockOption':
            return self.initialize_stockoption()
        else:
            raise NameError('There is no instrument with a name ' + self.instrument_type)

    def initialize_swaption(self):
        use_keys = ['sigma', 'run_time', 'exercises', 'tenor', 'strike',
                    'option_type', 'mean_reversion', 'forward_rates']
        if all(key in self.data for key in use_keys):
            return SwapOption(self.data['sigma'], self.data['run_time'], self.data['exercises'],
                              self.data['tenor'], self.data['strike'], self.data['option_type'],
                              self.data['mean_reversion'], self.data['forward_rates'])
        else:
            raise KeyError("Not all input parameters are available. Check Parameters: " + str(use_keys))

    def initialize_stockoption(self):
        use_keys = ['start_value', 'sigma', 'mue', 'run_time', 'exercises', 'strike', 'option_type']
        if all(key in self.data for key in use_keys):
            return StockOption(self.data['start_value'], self.data['sigma'], self.data['mue'], self.data['run_time'],
                               self.data['exercises'], self.data['strike'], self.data['option_type'])
        else:
            raise KeyError("Not all input parameters are available. Check Parameters: " + str(use_keys))
