import alpaca_trade_api as alpca
from helpers.api_init import initialize_api


class Trader:

    # Move this into a separate class and have it return an active account
    def __init__(self, api) -> None:
        self.ticker = "SPY"
        self.posiion = 0
        self.last_price = "1"
        self.current_order = None
        self.api = api

    def submit_order(self, quantity) -> None:
        """

        :param quantity:
        :return: None
        """
        # Cancel the current order before placing a new one
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        delta = quantity - self.posiion

        # If we already have the desired # of shares, do nothing
        if delta == 0:
            return
        elif delta > 0:
            self.current_order = self.api.submit_order(self.ticker, delta,
                                                       "buy", "limit", "day",
                                                       self.last_price)
            print(f"Buying {delta} shares!!!!")
        else:
            self.current_order = self.api.submit_order(self.ticker, delta,
                                                       "sell", "limit", "day",
                                                       self.last_price)
            print(f"Selling {delta} shares!!!!")


if __name__ == '__main__':
    api = initialize_api()
    bot = Trader(api)
    bot.submit_order(100)
