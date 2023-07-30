import math
import random
import unittest
from ..pipeline import PipelineConcurrency
from ..pipeline_shm import PipelineConcurrencyShm
from ..sequential import find_prime_under


class TestPrimeSieve(unittest.TestCase):
    def test_prime_sieve(self):
        n = random.randint(10, 50)
        primes_seq = find_prime_under(n)
        for v in primes_seq:
            for x in range(2, int(math.sqrt(v)) + 1):
                self.assertGreater(v % x, 0)
        
        pipeline_concurrency = PipelineConcurrency(n)
        self.assertEqual(primes_seq, pipeline_concurrency.execute())
        pipeline_concurrency_shm = PipelineConcurrencyShm(n)
        self.assertEqual(primes_seq, pipeline_concurrency_shm.execute())

