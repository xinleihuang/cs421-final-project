import math
import multiprocessing
from multiprocessing.shared_memory import ShareableList
from typing import Tuple


"""
implement Sieve of Eratosthenes via pipeline concurrency with shared memory
it splits the process into two stages
stage_0: find the first k primes starting in [2, upper_limit] in brute force
stage_1: for each prime found in stage_0, start the sieve process from it. Assume
         there are 3 prime seeds to start from, three subtasks will be created running
         concurrently, but the total number of concurrent tasks cannot exceed
         the number of CPU's
"""
class PipelineConcurrencyAlten:
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
    different processes will edit the same list self.is_composite.
    Drawback of shared memory, it will slow down concurrency as only one worker is
    allowed to write the shared memory
    Advantage, sharing working progress will save redundant computations.
    """
    def _stage_1(self, prime_seed: int) -> None:
        # loop through numbers in [2, upper_limit]
        # to identify all composites
        # ideally num must be a prime, expanding from a prime like num * num, num * (num+1) ,,,
        for num in range(prime_seed, self.upper_limit + 1):
            if self.is_composite[num]:
                continue
            for factor in range(num, self.upper_limit // num + 1):
                self.is_composite[num*factor] = True
    

    def _stage_1_altern(self, prime_seed: int, left: int, right: int, composites: list[int]) -> list[bool]:
        # loop through numbers in [2, upper_limit]
        # to identify all composites
        # ideally num must be a prime, expanding from a prime like num * num, num * (num+1) ,,,
        if left > self.upper_limit:
            return
        is_composite = composites.copy()
        for num in range(prime_seed, left):
            if is_composite[num]:
                continue
            for factor in range(max(left // num, num), right // num + 1):
                val = num * factor
                if val <= self.upper_limit:
                    is_composite[num*factor] = True
        return is_composite

    def execute(self) -> None:
        is_composite = [False for _ in range(self.upper_limit + 1)]
        with multiprocessing.Pool(processes=self.processors) as pool:
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

            # pool.map(self._stage_1, seeds)
            for seed in seeds:
                left, segments = seed * seed, []
                segment_width = (self.upper_limit - left) // self.processors + 1
                while left <= self.upper_limit:
                    segments.append((seed, left, min(left + segment_width - 1, self.upper_limit), is_composite))
                    left += segment_width
                rlts = pool.starmap(self._stage_1_altern, segments)
                for j in range(len(segments)):
                    l, r = segments[j][1], segments[j][2]
                    for val in range(l, r+1):
                        if rlts[j][val]:
                            is_composite[val] = True

        primes = [x for x in range(2, self.upper_limit + 1) if not is_composite[x]]
        return primes

