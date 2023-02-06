from LU import FloatConverter
from LU.LU_decomposition import LUDecomposerService


class LUController:
    def __init__(self, method, A, B, converter: FloatConverter):
        self.__method = method
        self.__A = A
        self.__B = B
        self.__converter = converter

    def solve(self):
        solver = LUDecomposerService(self.__A, self.__B, self.__converter)
        if self.__method == "Doolittle":
            return solver.DooLittle_Decomposition()

        if self.__method == "Crout":
            return solver.croutDecomposition()
