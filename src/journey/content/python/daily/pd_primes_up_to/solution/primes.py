def primes_up_to(n):
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for multiple in range(i * i, n + 1, i):
                is_prime[multiple] = False
        i += 1
    primes = []
    for number in range(2, n + 1):
        if is_prime[number]:
            primes.append(number)
    return primes
