from abc import *

"""
Abstract class for a float converter, performs normalization of a float
then defines the abstract method "convert" for its children.
Allows for switching of converting algorithms during runtime.
"""


class FloatConverter(ABC):
    @staticmethod
    def _normalize(num: float) -> tuple[float, int]:
        """
        Protected static method to aid children classes' methods,
        normalizes a number and returns both normalized form
        and shifts done.

        :param num: Number to be normalized.
        :return: A tuple containing the normalized form of the input number and
         the number of shifts performed to normalize it.
        """
        # If zero, no normalization needed
        if num == 0:
            return 0.0, 0

        # variable to store shifts,
        # shifts left are negative, shifts right are positive.
        shifts = 0

        # If number magnitude is larger than 1.0
        if abs(num) > 1:
            # loop while the magnitude is larger than 1.0
            while abs(num) > 1:
                # shift number decimals one value right
                num /= 10
                shifts += 1
        # else if number magnitude is less than 0.1
        elif abs(num) < 0.1:
            # loop while the magnitude is less than 0.1
            while abs(num) < 0.1:
                # shift number decimals one value left
                num *= 10
                shifts -= 1
        # return shifted number and number of shifts done.
        return num, shifts

    @abstractmethod
    def convert(self, num):
        pass
