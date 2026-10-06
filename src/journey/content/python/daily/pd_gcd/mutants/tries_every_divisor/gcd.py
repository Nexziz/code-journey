def gcd(a, b):
    if a == 0 or b == 0:
        return a + b
    i = min(a, b)
    while i > 1:
        if a % i == 0 and b % i == 0:
            return i
        i -= 1
    return 1
