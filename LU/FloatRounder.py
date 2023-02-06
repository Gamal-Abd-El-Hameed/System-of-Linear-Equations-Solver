from LU.FloatConverter import FloatConverter


class FloatRounder(FloatConverter):
    def __init__(self, n: int):
        self.__precision = n

    @property
    def precision(self) -> int:
        return self.__precision

    @precision.setter
    def precision(self, n: int) -> None:
        self.__precision = n

    def __round_to_n_digits(self, num: float) -> float:
        """
        Function to convert a float number to an n-digit arithmetic float number, rounds off the last digit.

        :param num: Float number to convert to n-digit arithmetic float number.
        :return: Converted n-digit arithmetic rounded float number.
        """
        num, shifts = super()._normalize(num)

        # Calling round() twice is required to remove some very small propagation errors.
        res = round(round(num, self.precision) * 10 ** shifts, self.precision - shifts)
        return res

    def convert(self, num):
        return self.__round_to_n_digits(num)
