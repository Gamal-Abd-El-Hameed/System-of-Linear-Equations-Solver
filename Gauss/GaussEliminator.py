


"""
Class to instantiate objects that can solve
a system of linear equations of any size 
using the Gauss Elimination algorithm.
All mathematical operations are converted using the specified float converter
Time Complexity: O(n**3)
"""
from Gauss.FloatConverter import FloatConverter
from Gauss.pivot import partial_pivot
from Gauss.scale import scale


class GaussEliminator:
    def __init__(self, coefficient_matrix: list[list[float]], constants_matrix: list[float], float_converter: FloatConverter):
        self.__coeff = coefficient_matrix
        self.__const = constants_matrix
        self.__var = [0.0] * len(self.__const)
        self.__converter = float_converter
        self.__positions = list(range(0, len(coefficient_matrix)))

    @property
    def coeff(self) -> list[list[float]]:
        """
        Getter method for the coefficients matrix property

        :return: Currently set coefficients matrix.
        """
        return self.__coeff

    @coeff.setter
    def coeff(self, coefficient_matrix: list[list[float]]) -> None:
        """
        Setter method for the coefficients matrix property

        :param coefficient_matrix: Coefficients matrix to set as property of object.
        :return: None
        """
        self.__coeff = coefficient_matrix

    @property
    def const(self) -> list[float]:
        """
        Getter method for the constants matrix property

        :return: Currently set constants matrix.
        """
        return self.__const

    @const.setter
    def const(self, constants_matrix: list[float]) -> None:
        """
        Setter method for the constants matrix property

        :param constants_matrix: constants matrix to set as property of object.
        :return: None
        """
        self.__const = constants_matrix

    @property
    def var(self) -> list[float]:
        """
        Getter method for the variables matrix property

        :return: Currently set variables matrix.
        """
        return self.__var

    @property
    def converter(self) -> FloatConverter:
        """
        Getter method for the float converter property

        :return: Currently set converter.
        """
        return self.__converter

    @converter.setter
    def converter(self, float_converter: FloatConverter) -> None:
        """
        Setter method for the float converter property

        :param float_converter: float converter to set as property of object.
        :return: None
        """
        self.__converter = float_converter

    @property
    def positions(self) -> list[int]:
        """
        Getter method for the positions list property

        :return: Currently set positions list.
        """
        return self.__positions

    @positions.setter
    def positions(self, position_list: list[int]) -> None:
        """
        Setter method for the positions list property

        :param position_list: positions list to set as property of object.
        :return: None
        """
        self.__positions = position_list

    def __update_positions(self):
        """
        Private method to update the indices of the coefficients matrix and
        constants matrix rows to the current value of the positions list.

        :return: None
        """
        # loop for all rows in coefficients matrix
        for i in range(0, len(self.coeff)):
            # if position different from positions list
            if i != self.positions[i]:
                # swap coefficients row with row specified in positions list
                self.coeff[i], self.coeff[self.positions[i]] = self.coeff[self.positions[i]], self.coeff[i]
                # swap constant with constant specified in positions list
                self.const[i], self.const[self.positions[i]] = self.const[self.positions[i]], self.const[i]
                # reset positions list
                self.positions[self.positions[i]] = self.positions[i]
                self.positions[i] = i
                break

    def __check_empty_rows(self):
        """
        Private method to check if the coefficients matrix contains a zero row.
        Throws a ValueError exception if found.

        :return: None
        """
        # loop for all rows in coefficients matrix
        for i in range(0, len(self.coeff)):
            # if row absolute max is zero
            if max(self.coeff[i], key=abs) == 0.0:
                # throw exception
                raise ValueError("Zero row found, only unique solution systems are supported.")

    def __eliminate(self):
        """
        Private method to perform forward elimination of the coefficients matrix and
        subsequent modification to the rows of the coefficients matrix and constants matrix.

        :return: None
        """
        # loop for all diagonal elements in coefficients list
        for i in range(0, len(self.coeff)):
            # update positions list based on pivoting of scaled copy of coefficients matrix
            self.positions = partial_pivot(scale(self.coeff, self.converter, start_index=i), i)
            # update coefficients matrix indexing
            self.__update_positions()
            # loop for all rows after selected diagonal element in coefficients list
            for j in range(i + 1, len(self.coeff)):
                # check if element under pivot is zero
                if self.coeff[j][i] == 0:
                    # if zero, skip row.
                    continue
                # calculate multiplier for row based on selected diagonal element
                multiplier = self.converter.convert(self.coeff[j][i] / self.coeff[i][i])
                # loop for all columns in coefficients list
                for k in range(0, len(self.coeff[j])):
                    # do element - (multiplier x diagonal element)
                    self.coeff[j][k] = self.converter.convert(self.coeff[j][k] - self.converter.convert(self.coeff[i][k]*multiplier))
                # do constant - (multiplier x constant in same row as diagonal element)
                self.const[j] = self.converter.convert(self.const[j] - self.converter.convert(self.const[i] * multiplier))
            # try to find zero rows
            try:
                self.__check_empty_rows()
            # catch and throw exception if found
            except ValueError as err:
                raise err

    def __substitute(self):
        """
        Private method to perform backwards substitution using matrices post elimination.

        :return: None
        """
        # calculate last variable in variable list
        self.var[len(self.var) - 1] = self.converter.convert(self.const[len(self.const) - 1] / self.coeff[len(self.coeff) - 1][len(self.coeff) - 1])
        # loop for all rows in eliminated matrix (start from bottom and move up)
        for i in range(len(self.coeff) - 2, -1, -1):
            # initialize variable with constant of row
            sigma = self.const[i]
            # loop for all columns after diagonal element of row
            for j in range(len(self.coeff) - 1, i, -1):
                # do sum - (coefficient element x variable value)
                sigma = self.converter.convert(sigma - self.converter.convert(self.coeff[i][j]*self.var[j]))
            # divide sum by coefficient of row variable to obtain variable
            self.var[i] = self.converter.convert(sigma / self.coeff[i][i])

    def solve(self) -> list[float]:
        """
        Method to solve a system of linear equations stored in the object's
        provided attributes using the Gauss Elimination algorithm.

        :return: 1-Dimensional matrix (as list of float) containing calculated solution.
        """
        # try to eliminate provided matrix
        try:
            self.__eliminate()
        # catch and throw exception raised from finding a zero row
        except ValueError as err:
            raise err
        # do backwards substitution
        self.__substitute()
        # return calculated variable solutions
        return self.var
