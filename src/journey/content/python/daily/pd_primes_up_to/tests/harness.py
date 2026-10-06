import sys

from primes import primes_up_to

result = primes_up_to(int(sys.argv[1]))
print(len(result), result[-1] if result else "-")
