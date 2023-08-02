import math
import multiprocessing
from typing import Tuple


"""
implement Sieve of Eratosthenes via pipeline concurrency without shared memory
it splits the process into two stages
stage_0: find the first k primes starting in [2, upper_limit] in brute force
stage_1: for each prime found in stage_0, start the sieve process from it. Assume
         there are 3 prime seeds to start from, three subtasks will be created running
         concurrently, but the total number of concurrent tasks cannot exceed
         the number of CPU's
"""
class PipelineConcurrency:
    def __init__(self, upper_limit: int) -> None:
        self.upper_limit = upper_limit
        self.processors = min(multiprocessing.cpu_count(), self.upper_limit)

    """
    determine whether a num is a prime
    return 0 if it's a composite
    return the number itself if it's a prime
    """
    def _stage_0(self, target: int) -> int:
        for val in range(2, int(math.sqrt(target)) + 1):
            if target % val == 0:
                return 0
        return target

    """
    identify all composites in [prime_seed, upper_limit]
    return a boolean list, True -> composite, False -> prime
    """
    def _stage_1(self, prime_seed: int) -> list[bool]:
        is_composite = [False for _ in range(self.upper_limit + 1)]
        
        # loop through numbers in [2, upper_limit]
        # to identify all composites
        # ideally num must be a prime, expanding from a prime like num * num, num * (num+1) ,,,
        for num in range(prime_seed, self.upper_limit + 1):
            if is_composite[num]:
                continue
            for factor in range(num, self.upper_limit // num + 1):
                is_composite[num*factor] = True
        return is_composite

    def execute(self) -> None:
        with multiprocessing.Pool(processes=self.processors) as pool:
            """
            find first {self.processors} primes concurrently
            each prime will be used as the starting point of sieve
            """
            seeds, i = [], 2
            while len(seeds) < self.processors and i < self.upper_limit:
                segments = list(range(i, min(i + self.processors, self.upper_limit)))
                # apply self._stage_0 to each item in segments array
                # and run them concurrently
                rlts = pool.map(self._stage_0, segments)
                for target in rlts:
                    if target:
                        seeds.append(target)
                i += self.processors

            # run self._stage_1 against each prime seed concurrently
            composite_segments = pool.map(self._stage_1, seeds)
            primes = []
            """
            for each number in [2, upper_limit], if none of composite_segment says it's a composite,
            this number is a prime
            """
            for i in range(2, self.upper_limit+1):
                val = False
                for segment in composite_segments:
                    if segment[i]:
                        val = True
                        break
                if not val:
                    primes.append(i)
            return primes
