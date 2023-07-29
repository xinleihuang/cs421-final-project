# merge sort concurrently
import multiprocessing
from typing import Tuple


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
