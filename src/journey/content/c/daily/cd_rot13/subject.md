# Rot 13

## Assignment

Write a program that takes one string and prints it encoded with ROT13: every
letter is replaced by the letter 13 places further along the alphabet, wrapping
around from `z` back to `a`. Case is kept. Everything that is not a letter is
printed unchanged. End with a newline.

    $ ./rot13 "Hello, World!"
    Uryyb, Jbeyq!

If the program does not receive exactly one argument, it prints only a newline.

## Turn in

- Files: `rot13.c`
- Allowed functions: `write`
