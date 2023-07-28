import time
from prime_sieve import sequential
from prime_sieve.pipeline import PipelineConcurrency


def main() -> None:
    upper_limit = input("find all primes not greater than: ")

    st_sequential = time.time()
    primes_by_sequential = sequential.find_prime_under(upper_limit=int(upper_limit))
    et_sequential = time.time()
    print('sequential time@ms=', (et_sequential - st_sequential) * 1000, '#primes=', len(primes_by_sequential))

    pipeline_concurrency = PipelineConcurrency(upper_limit=int(upper_limit))
    st_sequential = time.time()
    primes_by_pipeline = pipeline_concurrency.execute()
    et_sequential = time.time()
    print('pipeline time@ms=', (et_sequential - st_sequential) * 1000, '#primes=', len(primes_by_pipeline))


if __name__ == '__main__':
    main()