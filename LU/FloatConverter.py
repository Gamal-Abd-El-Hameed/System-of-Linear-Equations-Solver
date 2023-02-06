from abc import *

class FloatConverter(ABC):
    @staticmethod
    def _normalize(num: float) -> tuple[float, int]:
        """
        Private function to aid other module functions,
        normalizes a number and returns both normalized form
        and shifts done.

        :param num: Number to be normalized.
        :return: A tuple containing the normalized form of the input number and
         the number of shifts performed to normalize it.
        """
        if num == 0:
            return 0.0, 0
        shifts = 0
        if abs(num) > 1:
            while abs(num) > 1:
                num /= 10
                shifts += 1
        elif abs(num) < 0.1:
            while abs(num) < 0.1:
                num *= 10
                shifts -= 1
        return num, shifts

    @abstractmethod
    def convert(self, num):
        pass
