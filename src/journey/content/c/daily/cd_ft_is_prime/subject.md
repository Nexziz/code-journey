# Is it prime?

Daily · uses levels 1 to 5

## Assignment

Write a function that tells whether a number is prime:

    int ft_is_prime(int nb);

Return `1` if `nb` is prime and `0` otherwise. A prime has exactly two divisors:
1 and itself, so 0, 1 and negative numbers are not prime. The function prints
nothing.

## Things to think about

The tests include numbers close to two billion, and each run has a few seconds.
Trying every divisor up to `nb` is far too slow. Which divisors can you skip? And
careful: `i * i` overflows an `int` for big `i`; compare `i <= nb / i` instead.

## Turn in

- Files: `ft_is_prime.c`
- Allowed functions: none
