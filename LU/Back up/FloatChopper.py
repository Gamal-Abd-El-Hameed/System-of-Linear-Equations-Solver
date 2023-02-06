from LU.FloatConverter import FloatConverter


class FloatChopper(FloatConverter):
    def __init__(self, n: int):
        self.__precision = n

    @property
    def precision(self) -> int:
        return self.__precision

    @precision.setter
    def precision(self, n: int) -> None:
        self.__precision = n

    def __chop_to_n_digits(self, num: float) -> float:
        """
        Function to convert a float number to an n-digit arithmetic float number, chops after the last digit.

        :param num: Float number to convert to n-digit arithmetic float number.
        :return: Converted n-digit arithmetic chopped float number.
        """
        num, shifts = super()._normalize(num)

        # Calling round() twice is required to remove some very small propagation errors.
        if num > 0:
            res = round(round(num - 0.5 * 10 ** (-1 * self.precision), self.precision) * 10 ** shifts,
                        self.precision - shifts)
        elif num < 0:
            res = round(round(num + 0.5 * 10 ** (-1 * self.precision), self.precision) * 10 ** shifts,
                        self.precision - shifts)
        else:
            res = 0
        return res

    def convert(self, num):
        return self.__chop_to_n_digits(num)
