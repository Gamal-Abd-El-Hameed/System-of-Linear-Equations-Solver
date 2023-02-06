def union(list1: list[str], list2: list[str]) -> list[str]:
    """
    Function that combines two lists of strings disregarding common elements.

    :param list1: First list of strings to check.
    :param list2: Second list of strings to check.
    :return: Combined list of elements without repetition.
    """
    # Make copy of first list
    copy1 = list1
    # Loop for all elements in second list copy
    for i in list2:
        # Check if element is in both lists' copies
        if not(i in copy1):
            # if not, add to first list copy
            copy1.append(i)
    # return modified first list copy
    return copy1
