# Negative, zero, positive

Level 4 · new skill: **conditions**

## Assignment

Go through the numbers from -3 to 3, in order. For each one print a single
letter: `N` if it is negative, `Z` if it is zero, `P` if it is positive. End with
a newline. The output must be:

    NNNZPPP

## What you need to know

`if` runs a block only when its condition is true. `else if` and `else` cover
the other cases. This prints `E` for even numbers and `O` for odd ones:

    if (n % 2 == 0)
        write(1, "E", 1);
    else
        write(1, "O", 1);

Comparisons: `==` equal, `!=` different, `<` `>` `<=` `>=`. Mind the doubled
equals sign: `=` stores a value, `==` compares.

## Turn in

- Files: `signs.c`
- Allowed functions: `write`
