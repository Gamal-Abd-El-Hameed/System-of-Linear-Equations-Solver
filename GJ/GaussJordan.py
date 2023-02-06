from GJ.FloatConverter import *
from GJ.pivot import partial_pivot
from GJ.scale import scale


class Gauss_Jordan:

    def __init__(self, A, b, float_converter: FloatConverter):
        self.A = A
        self.b = b
        self.converter = float_converter
        self.positions = list(range(0, len(self.A)))

    def solve(self):
        """
        The method that combine pivoting and scaling, elimination,
        normalization to solve the equations and return the values
        """
        try:
            self.elimination()
        except ValueError as error:
            raise error
        self.normalize()
        return self.b

    def set_aug(self, A, b):  # setter method for the coefficient and constant matrices i.e the augmented matrix
        self.A = A
        self.b = b

    def get_aug(self):  # getter method for the coefficient and constant matrices
        return self.A, self.b

    def converter(self):  # getter method for the float converter
        return self.converter

    def converter(self, float_converter: FloatConverter):  # setter method for the float converter
        self.converter = float_converter

    def update_positions(self):
        # loop for all rows in coefficients matrix
        for i in range(0, len(self.A)):
            # if position different from positions list
            if i != self.positions[i]:
                # swap coefficients row with row specified in positions list
                self.A[i], self.A[self.positions[i]] = self.A[self.positions[i]], self.A[i]
                # swap constant with constant specified in positions list
                self.b[i], self.b[self.positions[i]] = self.b[self.positions[i]], self.b[i]
                # reset positions list
                self.positions[self.positions[i]] = self.positions[i]
                self.positions[i] = i
                break

    def checkEmptyRow(self, rowIndex):  # method to check if there is an empty row
        temp_sum = 0
        for coefficient in self.A[rowIndex]:
            temp_sum += abs(coefficient)
        if temp_sum == 0:
            raise ValueError("Error, empty row exists!")

    def elimination(self):  # method perform the elimination step for all equation except pivot equations
        for i in range(len(self.A[0])):

            # perform pivoting and scaling to the augmented matrix
            self.positions = partial_pivot(scale(self.A, self.converter, start_index=i), i)
            self.update_positions()
            for j in range(len(self.A[0])):  # skip pivot equation from elimination
                if i == j:
                    continue
                factor = self.converter.convert(self.A[j][i] / self.A[i][i])  # calculate the multiplier
                # perform the equations subtraction step on both the coefficient and constant matrix
                for k in range(i, len(self.A[0])):
                    self.A[j][k] = self.converter.convert(self.A[j][k] - self.converter.convert(factor * self.A[i][k]))
                try:
                    self.checkEmptyRow(j)
                except ValueError as error: # throw error if an empty row exists
                    raise error
                self.b[j] = self.converter.convert(self.b[j] - factor * self.b[i])

    def normalize(self):  # method to perform normalization after elimination
        for i in range(len(self.A[0])):
            self.b[i] = self.converter.convert(self.b[i] / self.A[i][i])  # divide by the diagonal element
