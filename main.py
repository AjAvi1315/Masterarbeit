from Test import PricingExamplesMC
from InstrumentInitializer import InstrumentInitializer

if __name__ == '__main__':
    paths = 10

    """Example Stockoption"""
    data_stock = PricingExamplesMC.stock_option_test()
    instrument = InstrumentInitializer('StockOption', data_stock)
    stock_option = instrument.initialize()
    v_stock = stock_option.pricer_monte_carlo(paths)

    print('Fair Value for Stock Option')
    print(v_stock)

    """Example Swaption"""
    data_swap = PricingExamplesMC.swap_option_test()
    instrument = InstrumentInitializer('SwapOption', data_swap)
    swap_option = instrument.initialize()
    v_swap = swap_option.pricer_monte_carlo(paths)

    print('Fair Value for Swaption')
    print(v_swap)



