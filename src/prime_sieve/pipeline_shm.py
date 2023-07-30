import math
import multiprocessing
from multiprocessing.shared_memory import ShareableList
from .sequential import find_prime_under_with_seed
from typing import Tuple


class PipelineConcurrencyShm:
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

    def _stage_1(self, prime_seed: int) -> None:
        # loop through numbers in [2, upper_limit]
        # to identify all composites
        # ideally num must be a prime, expanding from a prime like num * num, num * (num+1) ,,,
        for num in range(prime_seed, self.upper_limit + 1):
            if self.is_composite[num]:
                continue
            for factor in range(num, self.upper_limit // num + 1):
                self.is_composite[num*factor] = True

    def execute(self) -> None:
        self.is_composite = ShareableList([False for _ in range(self.upper_limit + 1)])
        with multiprocessing.Pool(processes=self.processors) as pool:
            seeds, i = [], 2
            while len(seeds) < self.processors and i < self.upper_limit:
                segments = list(range(i, min(i + self.processors, self.upper_limit)))
                rlts = pool.map(self._stage_0, segments)
                for target in rlts:
                    if target:
                        seeds.append(target)
                i += self.processors

            pool.map(self._stage_1, seeds)
        primes = [x for x in range(2, self.upper_limit + 1) if not self.is_composite[x]]
        self.is_composite.shm.close()
        self.is_composite.shm.unlink()
        return primes


class PipelineConcurrencySlow:
    def __init__(self, upper_limit: int) -> None:
        self.upper_limit = upper_limit
        self.is_composite = [False for _ in range(upper_limit + 1)]

    def _stage_0(self, batch: int) -> None:
        self.segments = [(i+1, min(i + batch, self.upper_limit)) for i in range(1, self.upper_limit, batch)]

    def _stage_1(self, l_boundary: int, r_boundary: int) -> Tuple[int, list[bool]]:
        is_composite = [False for _ in range(r_boundary - l_boundary + 1)]
        for factor in range(2, int(math.sqrt(r_boundary)) + 1):
            for num in range(max(factor * factor, (l_boundary + factor - 1) // factor * factor), r_boundary + 1, factor):
                is_composite[num - l_boundary] = True
        return l_boundary, is_composite

    def _stage_2(self, l_boundary: int, is_composite: list[bool]) -> None:
        for i in range(len(is_composite)):
            if is_composite[i]:
                self.is_composite[l_boundary + i] = True

    def execute(self) -> None:
        num_processes = min(multiprocessing.cpu_count(), self.upper_limit)
        batch = self.upper_limit // num_processes

        with multiprocessing.Pool(processes=num_processes) as pool:
            self._stage_0(batch=batch)
            rlts = pool.starmap(self._stage_1, self.segments)
            for l_boundary, is_composiste in rlts:
                self._stage_2(l_boundary=l_boundary, is_composite=is_composiste)
            return [x for x in range(2, self.upper_limit + 1) if not self.is_composite[x]]

