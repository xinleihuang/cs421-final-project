import inquirer
import random
import time
from merge_sort.sequential import merge_sort_seq
from merge_sort.divide_conquer import merge_sort_concurrent
from prime_sieve import sequential
from prime_sieve.pipeline import PipelineConcurrency
from prime_sieve.pipeline_shm import PipelineConcurrencyShm


def prime_sieve() -> None:
    upper_limit = input("find all primes not greater than: ")

    st_sequential = time.time()
    primes_by_sequential = sequential.find_prime_under(upper_limit=int(upper_limit))
    et_sequential = time.time()
    print('sequential time@ms=', (et_sequential - st_sequential) * 1000, '#primes=', len(primes_by_sequential))

    pipeline_concurrency = PipelineConcurrency(upper_limit=int(upper_limit))
    st_sequential = time.time()
    primes_by_pipeline = pipeline_concurrency.execute()
    et_sequential = time.time()
    print('concurrent time@ms=', (et_sequential - st_sequential) * 1000, '#primes=', len(primes_by_pipeline))
    pipeline_concurrency_shm = PipelineConcurrencyShm(upper_limit=int(upper_limit))
    st_sequential = time.time()
    primes_by_pipeline = pipeline_concurrency_shm.execute()
    et_sequential = time.time()
    print('concurrent time with shared memory@ms=', (et_sequential - st_sequential) * 1000, '#primes=', len(primes_by_pipeline))


def merge_sort() -> None:
    n = input("number of random integers to sort: ")
    numbers = list(range(int(n)))
    random.shuffle(numbers)
    st_sort_cc = time.time()
    merge_sort_concurrent(numbers)
    et_sort_cc = time.time()
    print('concurrent time@ms=', (et_sort_cc - st_sort_cc) * 1000)
    st_sort_seq = time.time()
    merge_sort_seq(numbers)
    et_sort_seq = time.time()
    print('sequential time@ms=', (et_sort_seq - st_sort_seq) * 1000)


def main() -> None:
    question = [
        inquirer.List('algo',
                      message="please select an algorithm to explore:",
                      choices=['prime sieve', 'merge sort'])
    ]
    algo = inquirer.prompt(question)['algo']
    print(algo)
    if algo == 'prime sieve':
        prime_sieve()
    else:
        merge_sort()


if __name__ == '__main__':
    main()