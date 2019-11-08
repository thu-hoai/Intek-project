def calculate_diagonal_difference(matrix):
    """
    Return the absolute diagonal difference of the specified matrix.

    @param matrix: a Python array representing a n-by-n square matrix such
    as for instance::

        [[0, 1, 2, 3],
        [5, 6, 7, 8],
        [9, 8, 7, 6],
        [5, 4, 3, 2]]

    @return: an integer representing the absolute diagonal difference
    of the specified matrix.
    """

    # Raise exception
    if matrix is None:
        return None

    if not isinstance(matrix, list):
        raise TypeError("Not an array")

    for row in matrix:
        if len(row) != len(matrix):
            raise TypeError("Not a square matrix")

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if not isinstance(matrix[i][j], int):
                raise TypeError ("Not an integer")

    # Initialize sum left-to-right diagonal and right-to-left diagonal
    diag_left_to_right = 0
    diag_right_to_left = 0
    # Sum for each diagonal
    for i in range(len(matrix)):
        diag_left_to_right += matrix[i][i]
        diag_right_to_left += matrix[i][len(matrix) - i - 1]

    return abs(diag_left_to_right - diag_right_to_left)

if __name__ == '__main__':
    matrix1 = [
    [0, 1, 2, 3],
    [5, 6, 7, 8],
    [9, 8, 7, 6],
    [5, 4, 3, 2]]
    try:
        print(calculate_diagonal_difference(matrix1))
    except:
        pass
    matrix2 = [
    [0, 1, 2, 3],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    [9, 8, 7, 6],
    [5, 4, 3, 2]]
    try:
        print(calculate_diagonal_difference(matrix2))
    except:
        pass

    matrix3 = [
    [0, 1, 2, 3, 5],
    [5, 6, 7, 8],
    [5, 6, 7, 8, 5],
    [9, 8, 7, 6],
    [5, 4, 3, 2]]
    try:
        print(calculate_diagonal_difference(matrix3))
    except:
        pass

    matrix4 = [
    [0, 1, 2, 3, 2],
    [5, 6, 7, 8],
    [9, 8, 7, 6],
    [9, 8, 7, 6],
    [5, 4, 3, '2']]
    try:
        print(calculate_diagonal_difference(matrix4))
    except:
        pass
