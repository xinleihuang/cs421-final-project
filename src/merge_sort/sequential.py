"""
Merge sort by sorting the list into 2 smaller ones
and merging sorted together recursively
"""

def merge(left: list[int], right: list[int]) -> list[int]:
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

def merge_sort_seq(nums: list[int]) -> list[int]:
    l = len(nums)
    if l < 2:
        return nums
    # left = merge_sort_seq(nums[:l//2])
    # right = merge_sort_seq(nums[l//2:])
    # return merge(left, right)
    buckets = [[x] for x in nums]
    while len(buckets) > 1:
        another = []
        for i in range(0, len(buckets), 2):
            another.append(merge(buckets[i], buckets[i+1] if i+1 < len(buckets) else []))
        buckets = another
    return buckets[0]

