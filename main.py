from datetime import datetime
from time import sleep
import alpaca_trade_api as alpca
from helpers.api_init import initialize_api
from strategy.strategy import Strategy
import json


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

    def __init__(self, alpaca_api: alpca, configuration: json) -> None:
        self.current_order = None
        self.api = alpaca_api
        self.strategy = Strategy(configuration)
        self.MAX_POSITION = 1000

    def main(self, crypto=False) -> None:
        """
        Runs the algorithm
        :return: None
        """
        print('Working...')
        if not crypto:
            while market_open():
                # Buys 100 shares if technical conditions are met
                self.place_orders(100)
                sleep(15)
                # Takes profit if stock is up 5%
                self.take_profit(5)
        else:
            # Not yet implemented
            pass

    def place_orders(self, quantity) -> None:
        """
        :return: None
        """
        # Cancel any current orders
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        # Need to make this more dynamic
        self.strategy.ma_strategy()
        self.strategy.rsi_strategy()

        for ticker in self.strategy.securities:
            if self.strategy.securities[ticker][1] == "buy":
                self.make_trade(ticker.get_ticker(), "buy", quantity,
                                ticker.get_data()["Close"].max() * 0.90)
                print(f"Buying {quantity} shares!")

            # Not yet doing short strats yet
            # elif self.strategy.securities[ticker][1] == "sell":
            #     self.make_trade(ticker.get_ticker(), "sell", quantity,
            #                     ticker.get_data()["Close"].min() * 1.10)
            #     print(f"Selling {quantity} shares!")

    def take_profit(self, percent: int) -> None:
        """
        Takes profits after a percent increase in stock price. Only doing long
        positions currently.
        :return: None
        """
        for ticker in self.strategy.securities:
            bid_price = self.api.get_last_quote(ticker.get_ticker())['bidprice']
            if bid_price >= ticker.get_average_price() * (1 + (percent / 100)):
                self.make_trade(ticker.get_ticker(), "sell",
                                self.api.get_position(ticker.get_ticker()),
                                bid_price * 1.05)

    def make_trade(self, ticker: str, side: str, quantity: int,
                   limit_price: float) -> None:
        """
        :param ticker: Stock to be purchased/sold
        :param quantity: Amount to be purchased/sold
        :param limit_price: Limit price
        :param side: Either buy or sell
        :return: None
        """
        if side == "sell":
            self.api.submit_order(symbol=ticker, qty=str(quantity), side="sell",
                                  type="limit", time_in_force="day",
                                  limit_price=str(limit_price))

        else:
            self.api.submit_order(symbol=ticker, qty=str(quantity), side="buy",
                                  type="limit", time_in_force="day",
                                  limit_price=str(limit_price))
            print(f"Buying {quantity} shares!!!!")


if __name__ == '__main__':
    api = initialize_api()
    config = "configurations/base_config.json"
    bot = Trader(api, config)
    bot.main()
