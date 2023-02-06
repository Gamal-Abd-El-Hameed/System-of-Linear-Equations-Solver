import re
from union import *

class InputHandler:

    def __init__(self, equations):
        self.eqs = equations

    def getAug(self):   # method that return the coefficient, variables, constants from the inserted equations
        # split the coefficient, variables and constants from the equations
        coff, var, B = self.extraction(self.eqs)
        # modify the matrices and order them
        try:
            coff, var, B = self.generateEquationsMatrices(coff, var, B)
        except Exception as error:
            raise error
        return coff, var, B

    def split_coff(self, term):  # method that split the coefficient from variable of one term
        for i in range(len(term)):
            # split when reaching the first character in the term
            if 65 <= ord(term[i]) <= 90 or 97 <= ord(term[i]) <= 122:
                # return 1 as coefficient if we don't find any thing as coefficient
                if i - 1 == -1:
                    return '1', term[i:]
                # return the variable and its corresponding coefficient
                return term[0:i - 1 if term[i - 1] == '*' else i], term[i:]
        return term, ""

    def adjustEquation(self, equation):     # clean the inserted equation and reformat it to be handled easily
        newEquation = equation.replace(' ', '').replace('--', '+')
        while '==' in newEquation:
            newEquation = newEquation.replace('==', '=')
        while '++' in newEquation:
            newEquation = newEquation.replace('++', '+')
        newEquation = newEquation[:1].replace('-', '-1*').replace('+', '1*') + newEquation[1:].replace('-', '+-1*')
        newEquation = newEquation.replace('=+', '=').replace('++', '+')
        # split at the equal operator and return left-hand-side and right-hand-side
        lhs = re.split('\+',re.split('=', newEquation)[0])
        rhs = re.split('\+',re.split('=', newEquation)[1])
        for i in range(len(rhs)):
            lhs.append('-1*'+rhs[i])
        return lhs

    def extraction(self, eqs):  # method that split the coefficient, variables and constants matrices from the equations
        coff = []
        var = []
        B = []
        for i in range(len(eqs)):
            cn = []
            vn = []
            if eqs[i] == "":
                continue
            lhs = self.adjustEquation(eqs[i])  # get the left and right hand side
            B.append(0.0)   # add the right-hand-side of the equation to constants matrix
            for j in range(len(lhs)):
                # split the coefficient and variable of each term
                coefficient, variable = self.split_coff(lhs[j])
                # if the term was literal subtract it from RHS
                if variable == "":
                    B[i] = float(B[i]) - float(eval(coefficient))
                    continue
                # append one coefficient and one variable
                cn.append(eval(coefficient))
                vn.append(variable)
            # row of coefficients and row of variables
            coff.append(cn)
            var.append(vn)
        return coff, var, B

    def generateEquationsMatrices(self, coff, var, B):   # method to modify the matrices and order them
        unique_var = []
        for i in range(len(var)):
            # get the unique variables from the all inserted equations
            unique_var = union(unique_var, var[i])
        for i in range(len(var)):
            for j in range(len(unique_var)):
                if len(var[i]) <= j:
                    # append 0 to the coefficient matrix in non-founded variables
                    var[i].append(unique_var[j])
                    coff[i].append(0)
                elif var[i][j] != unique_var[j]:
                    # if the current variable isn't equal to the corresponding in the unique variables
                    # swap it with the corresponding if exist in the list of variables
                    found = False
                    for k in range(j + 1, len(var[i])):
                        if var[i][k] == unique_var[j]:
                            var[i][j], var[i][k] = var[i][k], var[i][j]
                            coff[i][j], coff[i][k] = coff[i][k], coff[i][j]
                            found = True
                            break
                    # append 0 in its corresponding place if doesn't exist
                    if not found:
                        var[i].insert(j, unique_var[j])
                        coff[i].insert(j, 0)
                else:
                    # check if variables are duplicated
                    k = j + 1
                    while k < len(var[i]):
                        if var[i][k] == unique_var[j]:
                            # add their coefficients if it is duplicated
                            coff[i][j] = coff[i][j] + coff[i][k]
                            # remove the repeated variables
                            del coff[i][k]
                            del var[i][k]
                            k = k-1
                        k += 1
        if len(coff) != len(unique_var):
            raise Exception("Number of equations isn't equal to the number of variables")
        return coff, unique_var, B
