# Rot 13

Daily · uses levels 1 to 6

## Assignment

Write a program that takes one string and prints it encoded with ROT13: every
letter is replaced by the letter 13 places further along the alphabet, wrapping
around from `z` back to `a`. Case is kept. Everything that is not a letter is
printed unchanged. End with a newline.

    $ ./rot13 "Hello, World!"
    Uryyb, Jbeyq!

If the program does not receive exactly one argument, it prints only a newline.

## Things to think about

There are 26 letters, so applying ROT13 twice gets the original text back. The
`%` operator is the neat way to wrap around: think of a letter as a number from
0 to 25.

## Turn in

- Files: `rot13.c`
- Allowed functions: `write`
