from Gauss.FloatConverter import *
import copy


def scale(matrix: list[list[float]], converter: FloatConverter, constants: list[float] = None, start_index: int = 0) -> list[list[float]] or tuple[list[list[float]], list[float]]:
    """
    Function to scale a coefficients matrix (and optionally a constants matrix as well).
    Divides each row of the matrices by the absolute greatest value in the coefficients matrix's row.
    Does not change any of the provided matrices, but instead copies them.

    :param matrix: The coefficients matrix (as list of list of float) to be scaled.
    :param converter: A float converter to convert float format into a custom float format.
    :param constants: (Optional, default = None) The constants matrix (as list of float) to be scaled
     along the coefficients matrix.
    :param start_index: (Optional, default = 0) Rows and columns of the coefficients matrix to skip scaling.
    :return: The scaled coefficients matrix (as list of list of float) and (if provided) the scaled constants matrix.
    """
    # get deep copy of provided matrix
    res = copy.deepcopy(matrix)

    # if a constants matrix is provided
    if constants is not None:
        # get deep copy of provided constants matrix
        res_sol = constants

    # loop for all rows in coefficients matrix starting from specified start point
    for i in range(start_index, len(res)):
        # get absolute max value of row
        row_max = max(res[i], key=abs)

        # loop for all columns in coefficients matrix starting from specified start point
        for j in range(start_index, len(res[i])):
            # divide element by row max and convert using provided converter
            res[i][j] = converter.convert(res[i][j] / row_max)
        # if a constants matrix is provided
        if constants is not None:
            # divide constant by coefficients matrix row max and convert using provided converter
            res_sol[i] = converter.convert(res_sol[i] / row_max)

    # if a constants matrix is provided
    if constants is not None:
        # return scaled coefficients matrix and constants matrix
        return res, res_sol

    # return scaled coefficients matrix
    return res
