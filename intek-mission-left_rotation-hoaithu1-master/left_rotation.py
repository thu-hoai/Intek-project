
def left_rotation(a):
    """
    Returns an array which elements have been rotated
    this number of times to the left.

    Parameters:
    ----------
    array of integers and a number:
        example: ([1, 7, 0, 4, 1, 9, 7, 1], 4)
        every other format will be raised as an error

    Return:
    -----------
    An array which elements have been rotated this number of times to the left.
    """

    # Raise error
    if len(a) != 2:
        raise TypeError("Not an array of integers and a number")

    if not isinstance(a[0], list):
        raise TypeError("Not an list of number")

    if not isinstance(a[1], int):
        raise TypeError("Not an interger")

    for i in range(len(a[0])):
        if not isinstance(a[0][i], int):
            raise TypeError("Not an interger")

    n = len(a[0])
    # Return a list on the left after cutting
    new_list1 = a[0][(a[1] % n):]
    # Return a list on the right after cutting
    new_list2 = a[0][:(a[1] % n)]
    # Concatenate 2 list
    return new_list1 + new_list2

if __name__ == '__main__':
    a1 = ([1, 7, 0, 4, 1, 9, 7, 1], 1)
    print(left_rotation(a1))

    a2 = ([1, 7, 0, 4, 1, 9, "7", 1], 1)
    try:
        print(left_rotation(a2))
    except:
        pass

    a3 = (1, 7, 0, 4, 1, 9, 7, 1, 1)
    try:
        print(left_rotation(a3))
    except:
        pass

    a4 = ([1, 7, 0, 4, 1, 9, 7, 1], "1")
    try:
        print(left_rotation(a4))
    except:
        pass
