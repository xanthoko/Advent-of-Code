#!/bin/python3

import math
import os
import random
import re
import sys


# Complete the arrayManipulation function below.
def arrayManipulation(n, queries):
    arr = [0] * n
    for query in queries:
        start, end, value = query
        for i in range(start, end + 1):
            arr[i - 1] += value
    return max(arr)


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    # nm = input().split()

    # n = int(nm[0])

    # m = int(nm[1])

    # queries = []

    # for _ in range(m):
    #     queries.append(list(map(int, input().rstrip().split())))

    queries = [[1, 2, 100], [2, 5, 100], [3, 4, 100]]
    n = 5
    result = arrayManipulation(n, queries)
    print(result)

    # fptr.write(str(result) + '\n')

    # fptr.close()
