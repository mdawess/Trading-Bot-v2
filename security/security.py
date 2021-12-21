import numpy as np
import pandas as pd
import yfinance as yf


class Security:
    """
    Class to manage details of stock/crypto securities
    """

    def __init__(self, ticker: str, period: str, interval: str) -> None:
        """
        Initializes a crypto security object
        :param ticker: Specific crypto currency to be analyzed
        :param period: Time period over which the data is needed
        :param interval: Frequency data should be reported
        """
        self._ticker = ticker
        self._period = period
        self._interval = interval
        self._data = yf.download(self._ticker, self._period, self._interval)

    def get_ticker(self) -> str:
        """
        :return: Ticker
        """
        return self._ticker

    def get_last_price(self) -> float:
        """
        :return: Last value within the 24hr period
        """
        return self._data['Close'].iloc[-1]

    def get_data(self) -> pd.DataFrame:
        """

        :return: Pandas DataFrame containing values from the inputted period
        at the specified interval
        """
        return self._data

    def update_period(self, new_period: str) -> None:
        """
        :param new_period:
        :return: None
        """
        self._data = yf.download(self._ticker, new_period, self._interval)
