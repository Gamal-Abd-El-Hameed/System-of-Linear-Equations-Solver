from LU.FloatConverter import FloatConverter
from LU.LU_decomposition import LUDecomposerService

"""
used to control flow of code considered entry point to LU decomposition module
method: name of algorithm user want to use
A: coffiecient matrix
B: Value vector
converter: class used for chopping and rounding
"""


class LUController:
    def __init__(self, method, A, B, converter: FloatConverter):
        self.__method = method
        self.__A = A
        self.__B = B
        self.__converter = converter

    #function used to access LU Decomposer service and pass input
    def solve(self):
        solver = LUDecomposerService(self.__A, self.__B, self.__converter)
        if self.__method == "Doolittle":
            return solver.DooLittle_Decomposition()
        elif self.__method == "Crout":
            return solver.croutDecomposition()
