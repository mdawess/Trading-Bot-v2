from typing import Dict
import pandas as pd
import pandas_ta as ta



class Stock:
    """
    A class for trading stocks
    """

    def __init__(self, tickers: Dict[str, pd.DataFrame] = None) -> None:
        """
        Initialize a new stock trading instance.

        :param tickers: Dictionary of stocks with their .csv files loaded
        """

        self.tickers = tickers

    def get_indicators(self) -> None:
        """
        Employ a trading strategy to trade stock(s)
        """
        for ticker in self.tickers:
            # Adds all the indicators to the individual dataframe
            self.tickers[ticker].ta.strategy()


df = pd.read_csv('Trading-Bot-v2/tests/TSLA.csv', sep=',')
tickers = {'tsla': df}

st = Stock(tickers)
st.get_indicators()
st.tickers['tsla'].tail()


