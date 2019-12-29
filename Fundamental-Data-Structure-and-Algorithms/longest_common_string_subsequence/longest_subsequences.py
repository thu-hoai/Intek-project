
def longestStringSubsequence(s1, s2):
    """
    Take strings s1, s2 and returns the longest common subsequence
    of s1 and s2

    Parameters:
    -----------------
    s1
        string
    s2
        string

    Return:
    --------------------
    The longest common subsequence
        String type
        The longest common subsequence is the longest sequence of chars
        (case sensitive) such that all of them appear in both of the string,
        possibly with others chars in between.

    Method:
    -------------------------
    This below function based on instruction as below link
    https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

    """
    # Raise errors
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Not a string")

    # Create the array to store common subsequences of given strings
    matrix = [["" for x in range(len(s2))] for x in range(len(s1))]
    # Compare the each element of s1 s2
    for i in range(len(s1)):
        for j in range(len(s2)):
            # In case of each elements are the same:
            # Sequence matrix[i-1][j-1]) is extended by
            # the match element s1[i]
            if s1[i] == s2[j]:
                if i == 0 or j == 0:
                    matrix[i][j] = s1[i]
                else:
                    matrix[i][j] = matrix[i-1][j-1] + s1[i]
            # In case of two elements are not the same:
            # the longer common subsequences is retained
            else:
                matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1], key=len)
    # Return the last element of the matrix
    return matrix[-1][-1]


if __name__ == '__main__':

    s01 = "directory"
    s02 = "secretary"
    try:
        print(longestStringSubsequence(s01, s02))
    except:
        pass

    s03 = "thisisatest"
    s04 = "testing123testing"
    try:
        print(longestStringSubsequence(s03, s04))
    except:
        pass

    s05 = "aaaa"
    s06 = "aa"
    try:
        print(longestStringSubsequence(s05, s06))
    except:
        pass

    s07 = 456
    s08 = "aasd235+6"
    try:
        print(longestStringSubsequence(s07, s08))
    except:
        pass
