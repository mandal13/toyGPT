# Helper functions for Byte Pair Encoding (BPE) Tokenization   


def getPairStats(byteList, pairStats = None):
    """
    Computes the frequency of consecutive byte pairs in a given list.

    This function iterates through a list of bytes and calculates how often 
    each pair of consecutive bytes occurs, storing the result in a dictionary. 
    If an existing `pairStats` dictionary is provided, it updates the counts 
    within that dictionary instead of creating a new one.

    Args:
        byteList (list): A list of bytes (or integers representing byte values) 
                         for which to compute pair frequencies.
        pairStats (dict, optional): An existing dictionary to update with 
                                    the frequency of byte pairs. Defaults to None,
                                    in which case a new dictionary is created.

    Returns:
        dict: A dictionary where keys are tuples representing consecutive byte pairs,
              and values are the frequencies of those pairs in the input list.

    Example:
        >>> byteList = [1, 2, 1, 2, 1, 3]
        >>> getPairStats(byteList)
        {(1, 2): 2, (2, 1): 2, (1, 3): 1}

        >>> existingStats = {(1, 2): 1}
        >>> getPairStats([1, 2, 1], pairStats=existingStats)
        {(1, 2): 2, (2, 1): 1}
    """
    pairStats = {} if pairStats is None else pairStats
    for i in range(len(byteList) - 1):
        pair = (byteList[i], byteList[i + 1])
        if pair in pairStats:
            pairStats[pair] += 1
        else:
            pairStats[pair] = 1

    return pairStats



def merge(oldList, pair, idx):
    """
    Merges occurrences of a specified pair of elements in a list into a single new element.

    This function scans through a list and replaces consecutive occurrences of a given pair 
    with a specified value. Any other elements in the list remain unchanged.

    Args:
        oldList (list): The original list of elements to process.
        pair (tuple): A tuple containing two elements to search for in consecutive positions.
        idx: The value to replace the pair with when it is found.

    Returns:
        list: A new list where all instances of the specified pair are replaced by `idx`.

    Example:
        >>> oldList = [1, 2, 3, 1, 2, 4]
        >>> pair = (1, 2)
        >>> idx = 99
        >>> merge(oldList, pair, idx)
        [99, 3, 99, 4]
    """
    newList = []
    i = 0

    while i < len(oldList):
        if i < len(oldList) - 1 and oldList[i] == pair[0] and oldList[i + 1] == pair[1]:
            newList.append(idx)
            i += 2
        else:
            newList.append(oldList[i])
            i += 1
    return newList

if __name__ == "__main__":

    # Test the `getPairStats` and `merge` functions

    byteList = [1, 2, 1, 2, 1, 3]
    print(getPairStats(byteList))

    existingStats = {(1, 2): 1}
    print(getPairStats([1, 2, 1], pairStats=existingStats))

    oldList = [1, 2, 3, 1, 2, 4]
    pair = (1, 2)
    idx = 99
    print(merge(oldList, pair, idx))
    