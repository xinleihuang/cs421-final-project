import sys
import os


SCIRPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCIRPT_DIR))


import matplotlib.pyplot as plt
import random
import time
from ..merge_sort.divide_conquer import merge_sort_concurrent
from ..merge_sort.sequential import merge_sort_seq
from ..prime_sieve.pipeline import PipelineConcurrency
from ..prime_sieve.pipeline_alten import PipelineConcurrencyAlten
from ..prime_sieve.pipeline_shm import PipelineConcurrencyShm
from ..prime_sieve.sequential import find_prime_under


def performance_test_merge_sort():
    concurrent_times, sequential_times = [], []
    x = []
    for i in range(1, 22):
        n = 2**i
        x.append(n)
        nums = [x for x in range(1, n + 1)]
        random.shuffle(nums)
        st = time.time()
        merge_sort_concurrent(nums)
        concurrent_times.append((time.time() - st) * 1000)
        st = time.time()
        merge_sort_seq(nums)
        sequential_times.append((time.time() - st) * 1000)
        print("#num={} done".format(n))

    plt.plot(x, concurrent_times, label='concurrent')
    plt.plot(x, sequential_times, label='sequential')
    plt.legend()

    plt.xlabel("# of numbers")
    plt.ylabel("execution time ms")
    plt.show()


def performance_test_prime_sieve():
    concurrent_times, concurrent_alten_times, concurrent_shm_times, sequential_times = [], [], [], []
    x = []
    for i in range(1, 22):
        n = 2**i
        x.append(n)
        st = time.time()
        PipelineConcurrency(n).execute()
        concurrent_times.append((time.time() - st) * 1000)
        st = time.time()
        st = time.time()
        PipelineConcurrencyAlten(n).execute()
        concurrent_alten_times.append((time.time() - st) * 1000)
        st = time.time()
        PipelineConcurrencyShm(n).execute()
        concurrent_shm_times.append((time.time() - st) * 1000)
        st = time.time()
        find_prime_under(n)
        sequential_times.append((time.time() - st) * 1000)
        print("#num={} done".format(n))

    plt.plot(x, concurrent_times, label='concurrent')
    plt.plot(x, concurrent_alten_times, label='current_alt')
    plt.plot(x, concurrent_shm_times, label='current_shm')
    plt.plot(x, sequential_times, label='sequential')
    plt.legend()

    plt.xlabel("prime upper limit")
    plt.ylabel("execution time ms")
    plt.show()


if __name__ == '__main__':
    # performance_test_merge_sort()
    performance_test_prime_sieve()
    