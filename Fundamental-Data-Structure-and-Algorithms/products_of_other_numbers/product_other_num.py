def get_products_of_other_numbers(ls):

    """
    Return a list of products

    Parameter:
    ----------------
    a list of integers, for ex: [1, 7, 3, 4]

    Return:
    -----------------
    A list of integer:
        List of products or each index calculate the product of
        every integer except the integer at that index.
    """
    # Raise errors
    if not isinstance(ls, list):
        raise TypeError("Not a list")
    for i in range(len(ls)):
        if not isinstance(ls[i], int):
            raise TypeError("Not an integer")

    # Create a list to store products of integers
    list_of_products = []
    for num in ls:
        tmp = 1
        for i in range(len(ls)):
            if num != ls[i]:
                tmp *= ls[i]
        list_of_products.append(tmp)

    return list_of_products


if __name__ == '__main__':
    lst1 = [1, 7, 3, 4]
    try:
        print(get_products_of_other_numbers(lst1))
    except:
        pass
    lst2 = [1, "7", 3, 4]
    try:
        print(get_products_of_other_numbers(lst2))
    except:
        pass
    lst3 = (1, 7, 3, 4)
    try:
        print(get_products_of_other_numbers(lst3))
    except:
        pass
