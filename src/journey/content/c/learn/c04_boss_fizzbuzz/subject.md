# Boss: Fizz Buzz

Level 4 · boss

## Assignment

Go through the numbers 1 to 15, one per line:

- a multiple of 3 prints `Fizz`
- a multiple of 5 prints `Buzz`
- a multiple of both prints `FizzBuzz`
- anything else prints the number itself

The output starts like this:

    1
    2
    Fizz
    4
    Buzz

## What you need to know

Everything from levels 1 to 4. Two things to watch:

- Test the "both" case first, or `15` will print `Fizz` and stop.
- Numbers 10 to 15 have two digits. Split them with `/` and `%` like in the
  level 2 boss.

## Turn in

- Files: `fizzbuzz.c`
- Allowed functions: `write`
