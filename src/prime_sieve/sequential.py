def find_prime_under_with_seed(prime_seed: int, upper_limit: int) -> list[int]:
    # a list to track whether this number is a composite
    is_composite = [False for _ in range(upper_limit + 1)]
    
    # loop through numbers in [2, upper_limit]
    # to identify all composites
    for num in range(prime_seed, upper_limit + 1):
        if is_composite[num]:
            continue
        for factor in range(num, upper_limit // num + 1):
            is_composite[num*factor] = True
    
    # filter out composites
    primes = [x for x in range(prime_seed, upper_limit + 1) if not is_composite[x]]
    return primes


def find_prime_under(upper_limit: int) -> list[int]:
    # a list to track whether this number is a composite
    is_composite = [False for _ in range(upper_limit + 1)]
    
    # loop through numbers in [2, upper_limit]
    # to identify all composites
    for num in range(2, upper_limit + 1):
        if is_composite[num]:
            continue
        for factor in range(num, upper_limit // num + 1):
            is_composite[num*factor] = True
    
    # filter out composites
    primes = [x for x in range(2, upper_limit + 1) if not is_composite[x]]
    return primes