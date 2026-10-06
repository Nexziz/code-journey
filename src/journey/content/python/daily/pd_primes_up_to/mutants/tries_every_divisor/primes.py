def primes_up_to(n):
    primes = []
    for number in range(2, n + 1):
        is_prime = True
        for i in range(2, number):
            if number % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(number)
    return primes
