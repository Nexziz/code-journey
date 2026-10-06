# Greatest common divisor

Daily · uses levels 1 to 5

## Assignment

Write a function in `gcd.py`:

    def gcd(a, b):

It returns the greatest common divisor of two non-negative integers: the largest
number that divides both. `gcd(0, n)` is `n`. `math.gcd` is not allowed.

## Things to think about

Euclid's algorithm: `gcd(a, b)` is the same as `gcd(b, a % b)`, and you stop when
`b` reaches 0. Python can assign two variables at once: `a, b = b, a % b`.

## Turn in

- Files: `gcd.py`
