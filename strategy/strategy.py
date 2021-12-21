import json
from security.security import Security
from technicals import Technicals
from news import News
from helpers.configurations import load_config


class Strategy:
    """
    Forms an algorithm to predict direction of stock movement
    """

    def __init__(self, config: json) -> None:
        """
        :param config: File specifying tickers and strategy type
        """
        # Load the configuration
        self.config = load_config(config)

        self.securities = {}

        for ticker in self.config["tickers"]:
            stock = Security(ticker, self.config["period"],
                             self.config["interval"])
            if self.config["strategy"] == "technicals":
                self.securities[stock] = [Technicals(stock), None]
            else:
                self.securities[stock] = [News(stock), None]

    def ma_strategy(self) -> None:
        """
        :return: None
        """
        for security in self.securities:
            current_security = self.securities[security][0]
            if isinstance(current_security, Technicals):
                if (current_security.calculate_moving_average("10d") >
                        current_security.calculate_moving_average("20d")):
                    self.securities[security][1] = "buy"
                elif (current_security.calculate_moving_average("50d") >
                      current_security.calculate_moving_average("200d")):
                    self.securities[security][1] = "buy"
                else:
                    self.securities[security][1] = "hold"

    def rsi_strategy(self) -> str:
        """
        :return: "buy" if RSI below 30, "sell" if over 70 and "hold" otherwise
        """
        for security in self.securities:
            current_security = self.securities[security][0]
            if isinstance(current_security, Technicals):
                if current_security.calculate_rsi("14d") <= 30:
                    self.securities[security][1] = "buy"
                elif current_security.calculate_rsi("14d") >= 70:
                    self.securities[security][1] = "sell"
                else:
                    self.securities[security][1] = "hold"

    def volume_strategy(self) -> str:
        """
        :return: "buy" if volume is higher than average, "sell" if lower
        """
        pass
