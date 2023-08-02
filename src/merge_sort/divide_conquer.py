"""
Merge Sort via divide-conquer concurrently
"""
import multiprocessing
from typing import Tuple


"""
merge two sorted lists
"""
def merge(left: list[int], right: list[int]) -> list[int]:
    if not right:
        return left

    rlt = []
    i, j, L, R = 0, 0, len(left), len(right)
    while i < L or j < R:
        if i == L:
            rlt.append(right[j])
            j += 1
        elif j == R:
            rlt.append(left[i])
            i += 1
        elif left[i] <= right[j]:
            rlt.append(left[i])
            i += 1
        else:
            rlt.append(right[j])
            j += 1
    return rlt


"""
the list is divided into smaller ones to sort and merge recursively
when only one processor is available. Recursive calls continue until
the size of the list is 1, then merging process starts from bottom to top.
Deep down this can be treated as series of merging tasks. With multiple
processors, this problem can be solved by
    1). convert list[int] to list[list[int]] wrapping each integer in a list
    2). merge child lists 2*i and 2*i + 1, where i = 0, 1, ..., n//2, concurrently
    3). repeat step 2 until only one list left, which is the sorted one
"""
def merge_sort_concurrent(nums: list[int]) -> list[int]:
    N = len(nums)
    buckets = [[x] for x in nums]

    cpus = multiprocessing.cpu_count()
    
    with multiprocessing.Pool(processes=cpus) as pool:
        while len(buckets) > 1:
            tasks = []
            for i in range(0, len(buckets), 2):
                tasks.append((buckets[i], buckets[i+1] if i+1 < len(buckets) else []))
            buckets = pool.starmap(merge, tasks)

    return buckets[0]
