# Negative, zero, positive

Level 4 · new skill: **conditions**

## Assignment

Go through the numbers from -3 to 3, in order. For each one print a single
letter on the same line: `N` if it is negative, `Z` if it is zero, `P` if it is
positive. The output must be:

    NNNZPPP

## What you need to know

`if` runs its indented block only when its condition is true. `elif` and `else`
cover the other cases. This prints `E` for even numbers and `O` for odd ones:

    if n % 2 == 0:
        print("E", end="")
    else:
        print("O", end="")

Comparisons: `==` equal, `!=` different, `<` `>` `<=` `>=`. Mind the doubled
equals sign: `=` stores a value, `==` compares. Do not forget the colons.

## Turn in

- Files: `signs.py`
