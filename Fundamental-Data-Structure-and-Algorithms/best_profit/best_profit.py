
def get_max_profit(stock_prices):
    """
    Returns the best profit that could have been made from one purchase and one sale

    Parameter
    -----------
    stock_prices: a list of numbers
        list

    Return
    ------------
    the best profit
        int
    """
    # Raise errors
    if not isinstance(stock_prices, list):
        raise TypeError("Not a list")

    for i in range(len(stock_prices)):
        if isinstance(stock_prices[i], str):
            raise TypeError("Not a list of numbers")

    profit = [] # Initialize an empty list of profit posibility
    for j in range(len(stock_prices)):
        buy_price = stock_prices[j] # Assign buy_price
        # List of profit could have made from one purchase
        for i in range(len(stock_prices)):
            if stock_prices[i] > buy_price and i > j:
                profit.append(stock_prices[i] - buy_price)

    return max(profit)


if __name__ == '__main__':
    stock_prices1 = [10, 7, 5, 8, 11, 9]
    try:
        print(get_max_profit(stock_prices1))
    except:
        pass

    stock_prices2 = [10, 7, 5, 8, 11, 1, 12, 21]
    try:
        print(get_max_profit(stock_prices2))
    except:
        pass

    stock_prices3 = [13, 7, 5, 8, 11, 1]
    try:
        print(get_max_profit(stock_prices3))
    except:
        pass
    stock_prices4  = [45, 24, 35, 31, "40", 38, 11]
    try:
        print(get_max_profit(stock_prices4))
    except:
        pass
