from FloatConverter import *

"""
Child class of FloatConverter.
Objects of this instance are capable of
rounding a floating-point number to
n significant digits.
Does not transform into exponential form.
"""


class FloatRounder(FloatConverter):
    def __init__(self, n: int):
        self.__precision = n

    @property
    def precision(self) -> int:
        """
        Getter for the precision property

        :return: Current value of the precision property.
        """
        return self.__precision

    @precision.setter
    def precision(self, n: int) -> None:
        """
        Setter for the precision property

        :param n: New precision to set to the FloatRounder object
        :return: None
        """
        self.__precision = n

    def __round_to_n_digits(self, num: float) -> float:
        """
        Private method to convert a float number to an n-digit arithmetic float number,
        rounds off the last digit.

        :param num: Float number to convert to n-digit arithmetic float number.
        :return: Converted n-digit arithmetic rounded float number.
        """
        # call parent's normalize method
        num, shifts = super()._normalize(num)

        # round the normalized number to required digits of precision
        # then shift it back to its original form.
        # calling round() twice is required to remove some very small propagation errors from shifting.
        res = round(round(num, self.precision) * 10 ** shifts, self.precision - shifts)
        return res

    def convert(self, num):
        """
        Method to round a standard floating-point number to a
        floating-point number of exactly n precision.

        :param num: Floating-point number to round
        :return: Exact n precision floating-point number.
        """
        return self.__round_to_n_digits(num)
