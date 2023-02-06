def partial_pivot(matrix: list[list[float]], column: int) -> list[int]:
    """
    Function to calculate the absolute greatest value in a selected
    column of the provided matrix.

    :param matrix: The matrix(List of List of float) in which a column is to be evaluated.
    :param column: The index of the column to be evaluated.
    :return: A list containing the new positions of each row such that list[old_position] = new_position.
    """
    # initialize a list of numbers from 1 to (size of matrix)
    positions = list(range(0, len(matrix)))

    # variable to store absolute max value encountered
    max_val = 0
    # variable to store index of absolute max value encountered
    max_index = 0

    # loop for all rows in the matrix
    for i in range(column, len(matrix)):
        # if the absolute value of the element is greater than anything encountered before
        if abs(matrix[i][column]) > abs(max_val):
            # set max value to element
            max_val = matrix[i][column]
            # set max index to index of element
            max_index = i

    # swap index of the row containing pivot element with the index of the row containing greatest element
    positions[column], positions[max_index] = positions[max_index], positions[column]
    return positions
