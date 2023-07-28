import math
import multiprocessing
from typing import Tuple


class PipelineConcurrency:
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

