# Boss: is it prime?

Level 5 · boss

## Assignment

Write a function in `is_prime.py`:

    def is_prime(n):

It returns `True` if `n` is prime and `False` otherwise. A prime has exactly two
divisors, 1 and itself, so 0, 1 and negative numbers are not prime.

## What you need to know

Everything so far, in one function. Think about speed: the tests include numbers
around a billion, and a program that tries every divisor up to `n` would run for
minutes. If `n` has a divisor, it has one that is at most its square root. Which
loop condition expresses that without any outside function?

## Turn in

- Files: `is_prime.py`
