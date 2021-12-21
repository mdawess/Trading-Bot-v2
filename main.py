from datetime import datetime
from time import sleep
import alpaca_trade_api as alpca
from helpers.api_init import initialize_api
from strategy.strategy import Strategy


def market_open() -> bool:
    """
    Checks to see if the market is currently open
    :return: True iff the market is open
    """
    time = datetime.now()

    if (9, 30) <= (time.hour, time.minute) <= (16, 30):
        return True
    return False


class Trader:

    # Move this into a separate class and have it return an active account
    def __init__(self, api: alpca, config: json) -> None:
        self.current_order = None
        self.api = api
        self.strategy = Strategy(config)
        self.MAX_POSITION = 1000

    def place_orders(self, quantity) -> None:
        """

        :return: None
        """
        # Cancel any current orders
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        self.strategy.ma_strategy()
        self.strategy.rsi_strategy()

        for ticker in self.strategy.securities:
            if self.api.get_position < self.MAX_POSITION:
                if self.strategy.securities[ticker][1] == "buy":
                    self.api.submit_order(ticker.get_ticker(), quantity,
                                          "buy", "limit", "day",
                                          ticker.get_data()["Close"].iloc[
                                              -1] * 0.90)
                    print(f"Buying {quantity} shares!!!!")
            elif self.strategy.securities[ticker][1] == "sell":
                self.api.submit_order(ticker.get_ticker(), quantity,
                                      "sell", "limit", "day",
                                      ticker.get_data()["Close"].iloc[
                                          -1] * 1.10)

                print(f"Selling {quantity} shares!!!!")

    def main(self, crypto=False) -> None:
        """
        Runs the algorithm
        :return: None
        """
        if not crypto:
            while market_open():
                self.place_orders(100)
                sleep(15)
        else:
            self.place_orders(0.5)
            sleep(15)


if __name__ == '__main__':
    api = initialize_api()
    config = "configurations/base_config.json"
    bot = Trader(api, config)
    bot.main()
