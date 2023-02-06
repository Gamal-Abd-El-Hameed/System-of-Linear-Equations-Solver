import copy
import math

from GaussJaccobi.FloatConverter import FloatConverter


class GaussSeidil:

    def __init__(self, A, B, iterations, eps, initialGuess, float_converter: FloatConverter):
        self.A = A
        self.B = B
        self.iterations = iterations
        self.eps = eps
        self.newX = initialGuess
        self.converter = float_converter

    def getAbsoluteRelativeError(self, newValue, oldValue):  # method to calculate the relative error
        if (newValue == oldValue): return 0
        if (newValue == 0): return 100  # Assumption  instead of relative error = infinity
        ans = self.converter.convert(abs(self.converter.convert(
            self.converter.convert(newValue - oldValue) / newValue)))  # calculate the relative error
        return self.converter.convert(ans)

    def solve(self):
        finished = False
        for iteration in range(self.iterations):
            maxRelativeError = 0
            oldX = copy.deepcopy(self.newX)  # get copy of the new values

            for i in range(len(self.newX)):
                tempSum = 0
                for j in range(len(self.newX)):
                    # Skip the Coefficient of the UnKnown
                    if (i == j): continue

                    # Sum of products of other UnKnowns by their Coefficients
                    tempSum = self.converter.convert(tempSum + self.converter.convert(self.A[i][j] * self.newX[j]))

                # Store the new Value of the UnKnown
                self.newX[i] = self.converter.convert(self.converter.convert(self.B[i] - tempSum) / self.A[i][i])

            # Check Required Accuracy
            for i in range(len(self.newX)):
                relativeError = self.getAbsoluteRelativeError(self.newX[i], oldX[i])
                if maxRelativeError < relativeError:
                    maxRelativeError = relativeError

            if maxRelativeError < self.eps:  # end the iterations if we reach maximum relative error < eps
                finished = True
                break
            for i in range(len(self.newX)):
                if abs(self.newX[i] - oldX[i]) >= 10**10:
                    raise ValueError("Error! Diverge!!")

        return self.newX


