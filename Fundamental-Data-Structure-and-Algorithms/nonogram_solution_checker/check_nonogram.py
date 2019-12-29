
def check_solution_row(array):
    """
    Return a tuple of all count rows of solution

    Parameter: an array as below instance
    -------------
        tuple
        solution1_true = (
        (0, 1, 0, 1, 0),
        (1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1),
        (0, 1, 1, 1, 0),
        (0, 0, 1, 0, 0)
        )

    Return:
    --------------
        tuple
        ((1, 1), (5,), (5,), (3,), (1,))
    """

    # Initialize a tuple o store the count of "1" of all rows
    all_row_list = ()
    # Check each value in given solution
    for i in range(len(array)):
        tmp_count = 0
        # Initialize a tuple o store the count of "1" of current rows
        each_row_count = ()
        for value in array[i]:
            if value == 1:
                tmp_count += 1
            else:
                if tmp_count != 0:
                    each_row_count += (tmp_count,)
                tmp_count = 0 # Restart tmp_count for every catching "0"
        if tmp_count != 0:
            each_row_count += (tmp_count,)
        all_row_list += (each_row_count,)
        # Restart all temporary value every other rows
        each_row_count = ()
        tmp_count = 0
    return all_row_list

def check_solution_column(arr):
    """
    Return a tuple of all count columns of solution

    Parameter: an array as below instance
    -------------
        tuple
        solution1_true = (
        (0, 1, 0, 1, 0),
        (1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1),
        (0, 1, 1, 1, 0),
        (0, 0, 1, 0, 0)
        )

    Return:
    --------------
        tuple
        ((2,), (4,), (4,), (4,), (2,))
    """

    # Initialize a tuple o store the count of "1" of all rows
    all_col_list = ()

    # Check each value in given solution
    for i in range(len(arr[0])):
        tmp_count = 0
        # Initialize a tuple o store the count of "1" of current cols
        each_col_count = ()
        for j in range(len(arr)):
            if arr[j][i] == 1:
                tmp_count += 1
            else:
                if tmp_count != 0:
                    each_col_count += (tmp_count,)
                tmp_count = 0
        if tmp_count != 0:
            each_col_count += (tmp_count,)
        all_col_list += (each_col_count,)
        # Re restart all temporary value every other cols
        each_col_count = ()
        tmp_count = 0

    return all_col_list

def is_nonogram_resolved(specifications, solution):
    """
    Check if suggested solution matches the nonogram's specifications

    Parameters:
    --------------
    specifications :
        two tuples as follows:

        specifications = (
        ((2,), (4,), (4,)),
        ((1,), (3,), (3,), (2,), (1,))2
        )

        solution = (
        (0, 1, 0,),
        (1, 1, 1),
        (1, 1, 1),
        (0, 1, 1),
        (0, 0, 1)
        )

    Return:
    ---------------
    True
        the suggested solution matches the nonogram's specifications
    False
        otherwise
    """
    # Raise exception
    if specifications is None or solution is None:
        return None

    if not isinstance(specifications, tuple):
        raise TypeError('Your specifications is not a tuple')

    if not isinstance(solution, tuple):
        raise TypeError('Your solution is not a tuple')

    if len(specifications) != 2:
        raise ValueError("An inappropriate solution or specifications")

    if len(specifications[1]) != len(solution) \
        or len(specifications[0]) != len(solution[0]):
        raise ValueError('An inappropriate solution or specifications')

    # Check for both rows and columns
    if check_solution_row(solution) == specifications[1] and \
        check_solution_column(solution) == specifications[0]:
        return True
    return False

if __name__ == '__main__':
    specifications1 = (
    ((2,), (4,), (4,), (4,), (2,)),
    ((1, 1), (5,), (5,), (3,), (1,))
    )
    solution1_true = (
    (0, 1, 0, 1, 0),
    (1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1),
    (0, 1, 1, 1, 0),
    (0, 0, 1, 0, 0)
    )
    try:
        print(is_nonogram_resolved(specifications1, solution1_true))
    except:
        pass
    solution1_false = (
    (0, 1, 0, 0, 0),
    (1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1),
    (0, 1, 1, 1, 0),
    (0, 0, 1, 0, 0)
    )
    try:
        print(is_nonogram_resolved(specifications1, solution1_false))
    except:
        pass

    specifications_15x15 = (
    ((2, 4, 2, 1), (3, 2, 1, 1, 1), (1, 2, 1, 1, 2, 1), (1, 1, 1, 1, 5),
     (1, 1, 1, 2, 3), (1, 8, 3), (6, 3, 2), (5, 1, 2), (1, 1, 2, 1, 1),
     (3, 2, 1, 3), (1, 1, 1, 2), (1, 1, 2, 4, 1), (1, 2, 1, 1, 2),
     (1, 4, 2, 3), (9, 1, 2)),
    ((3, 1, 1, 1, 1), (2, 1, 4, 2), (4, 2, 4, 1), (1, 6, 1), (1, 3, 4),
     (7, 1, 5), (1, 5, 2), (1, 2, 1, 1, 4), (2, 3, 1, 2, 1), (4, 1, 3),
     (1, 2, 1, 2), (1, 2, 2), (8, 2, 3), (5, 6), (3, 2, 1))
    )
    solution_15x15 = (
    (0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1),
    (1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1),
    (1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1),
    (0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1),
    (0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1),
    (1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1),
    (1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1),
    (0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0),
    (0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1),
    (1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1),
    (0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0),
    )
    try:
        print(is_nonogram_resolved(specifications_15x15, solution_15x15))
    except:
        pass
