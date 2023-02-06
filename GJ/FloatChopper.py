from GJ.FloatConverter import FloatConverter

"""
Child class of FloatConverter.
Objects of this instance are capable of
rounding a floating-point number to
n significant digits.
Does not transform into exponential form.
"""


class FloatChopper(FloatConverter):
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

    def __chop_to_n_digits(self, num: float) -> float:
        """
        Private method to convert a float number to an n-digit arithmetic float number,
         chops after the last digit.

        :param num: Float number to convert to n-digit arithmetic float number.
        :return: Converted n-digit arithmetic chopped float number.
        """
        # call parent's normalize method
        num, shifts = super()._normalize(num)

        # chop the normalized number to required digits of precision
        # then shift it back to its original form.
        # Calling round() twice is required to remove some very small propagation errors.
        if num > 0:
            # for positive numbers chopping is done by rounding (the number - 0.5)
            res = round(round(num - 0.5 * 10 ** (-1 * self.precision), self.precision) * 10 ** shifts,
                        self.precision - shifts)
        elif num < 0:
            # for negative numbers chopping is done by rounding (the number + 0.5)
            res = round(round(num + 0.5 * 10 ** (-1 * self.precision), self.precision) * 10 ** shifts,
                        self.precision - shifts)
        else:
            # for zero no chopping needed
            res = 0
        return res

    def convert(self, num):
        """
        Method to chop a standard floating-point number to a
        floating-point number of exactly n precision.

        :param num: Floating-point number to chop
        :return: Exact n precision floating-point number.
        """
        return self.__chop_to_n_digits(num)
