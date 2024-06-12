from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets you want to trade.
        self.tickers = ["AAPL"]

    @property
    def interval(self):
        # Set the data interval (e.g., daily data)
        return "1day"

    @property
    def assets(self):
        # Return the list of tickers
        return self.tickers

    def run(self, data):
        # Initialize the allocation with no holdings
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        # Iterate through each ticker to make decisions
        for ticker in self.tickers:
            # Get the MACD indicators for the ticker
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            # Check if we have enough data to proceed
            if macd_data and len(macd_data["MACD"]) > 2 and len(macd_data["signal"]) > 2:
                # Get the latest MACD and signal values
                macd_line = macd_data["MACD"][-1]
                signal_line = macd_data["signal"][-1]
                prev_macd_line = macd_data["MACD"][-2]
                prev_signal_line = macd_data["signal"][-2]
                
                # Generate signals based on MACD crossover
                if macd_line > signal_line and prev_macd_line <= prev_signal_line:
                    # Signal to buy
                    allocation_dict[ticker] = 1.0
                    log(f"Buying {ticker}")
                elif macd_line < signal_line and prev_macd_line >= prev_signal_line:
                    # Signal to sell
                    allocation_dict[ticker] = 0
                    log(f"Selling {ticker}")
                # Else, hold the current position. No action is necessary.

        # Return the calculated target allocations
        return TargetAllocation(allocation_dict)