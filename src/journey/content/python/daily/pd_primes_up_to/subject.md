# All the primes

Daily · uses levels 1 to 5

## Assignment

Write a function in `primes.py`:

    def primes_up_to(n):

It returns a **list** of all the prime numbers from 2 up to `n` (included), in
increasing order. For `n` below 2 it returns an empty list.

    primes_up_to(10)    ->  [2, 3, 5, 7]

## What you need to know

A list holds several values in order: `numbers = [3, 1, 2]`. `numbers.append(5)`
adds to the end, `numbers[0]` is the first element and `len(numbers)` counts them.
The test prints how many primes you found and the last one.

## Things to think about

Testing each number with a loop of divisors works for small limits but is slow for
big ones. The sieve of Eratosthenes is much faster: keep a list of `True` flags,
one per number, and for each prime found, cross out all its multiples.

## Turn in

- Files: `primes.py`
