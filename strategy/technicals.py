from security.security import Security


# Sources:
# stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas

class Technicals:
    """
    Common technical indicators for trading
    """

    def __init__(self, security: Security) -> None:
        """
        Initializes a technical indicator object for a specific security
        :param ticker: Stock/crypto to be analysed
        :param period: Time frame over which the stock will be analysed
        :param interval: Frequency of data
        """
        self.security = security

    def calculate_moving_average(self, period: str) -> float:
        """
        :param period: Time frame for MA, usually 50, 100, 200, 250 days
        :return: The average of a stock over a given period
        """
        self.security.update_period(period)
        return self.security.get_data()['Close'].mean()

    def calculate_rsi(self, period: int) -> float:
        """
        :param period: Time frame for the moving average
        :return: RSI
        """
        # From: StackOverflow
        close = self.security.get_data()['Adj Close']
        # Get the difference in price from previous step
        delta = close.diff()
        # Get rid of the first row
        delta = delta[1:]
        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.clip(lower=0), delta.clip(upper=0).abs()

        if down.empty:
            return 100
        elif up.empty:
            return 0
        else:
            roll_up = up.rolling(period).mean()[-1]
            roll_down = down.rolling(period).mean()[-1]
            rs = roll_up / roll_down
            rsi = 100 - (100 / (1 + rs))
            return rsi

    def calculate_average_volume(self, period: str) -> float:
        """
        :param period: Time frame for volume
        :return:
        """
        self.security.update_period(period)
        return self.security.get_data()['Volume'].mean()
