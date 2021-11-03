from typing import List
import pandas as pd
import numpy as np


class Technicals:
    """
    A class of main technical indicators to analyze and predict stock
    performance. Indicators include moving average (ma), relative strength
    index (rsi), standard deviation (sd) and average volume (av).

    Public Attributes
    - ticker: the specific stock to be analyzed

    TODO: Find a data source to pull from
    TODO: Write methods to calculate and return required data
    """

    def __init__(self, ticker) -> None:
        """
        Initializes technical analysis for the given ticker.
        """
        self.ticker = ticker

    def ma(self, num_days: int, period: int) -> List[float]:
        """
        Returns the moving average for num_days over period. Strategy will be
        to compare when one ma crosses another. Specifically when a short term
        ma crosses a long term one.

        Note: period > num_days
        """
        pass

    def rsi(self) -> int:
        """
        Returns the RSI for the given ticker. Strategy will be to compare to
        traditional ranges of > 70 and < 30 which indicate overbought and
        oversold respectively.
        """
        pass

    def sd(self, num_days: int) -> float:
        """
        Returns the sd for the stock over num days. Strategy will be to use
        this in alongside other indicators to predict magnitude of up or down
        shift.
        """
        pass

    def av(self, num_days) -> int:
        """
        Returns the average volume over num_days. Strategy will be to use this
        in alongside other indicators to predict magnitude of up or down
        shift.
        """
        pass
