import random
import unittest
from ..divide_conquer import merge_sort_concurrent
from ..sequential import merge_sort_seq


class TestMergeSort(unittest.TestCase):
    def test_merge_sort(self):
        nums = list(range(10))
        random.shuffle(nums)
        self.assertEqual(sorted(nums), merge_sort_seq(nums))
        self.assertEqual(sorted(nums), merge_sort_concurrent(nums))

    