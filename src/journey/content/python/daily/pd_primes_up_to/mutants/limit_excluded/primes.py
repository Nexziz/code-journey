def primes_up_to(n):
    primes = []
    for number in range(2, n):
        is_prime = True
        i = 2
        while i * i <= number:
            if number % i == 0:
                is_prime = False
                break
            i += 1
        if is_prime:
            primes.append(number)
    return primes
