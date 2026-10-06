# Count the vowels

Daily · uses levels 1 to 6

## Assignment

Write a program that counts the vowels (`a e i o u`, in either case) in its
argument and prints the count as a decimal number, followed by a newline.

    $ ./count_vowels "hello"
    2

If the program does not receive exactly one argument, it prints `0`.

## Things to think about

`write` cannot print an `int`: you must turn the count into characters yourself,
and the count can have several digits. A small function that prints a number
(like the boss of level 5) keeps `main` readable.

## Turn in

- Files: `count_vowels.c`
- Allowed functions: `write`
