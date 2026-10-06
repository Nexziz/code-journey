# The next letter

Level 2 · new skill: **variables**

## Assignment

Read one letter from the input and print the letter that comes 5 places after it
in the alphabet. You will only be given letters from `a` to `u` (or `A` to `U`).

    $ python3 next_letter.py
    f
    k

## What you need to know

A variable is a name for a value:

    letter = "f"
    count = 3

`input()` waits for a line of text and gives it back as a string:

    answer = input()

Every character has a number: `ord("a")` is 97 and `chr(97)` is `"a"`. So moving
along the alphabet is arithmetic: `chr(ord("a") + 1)` is `"b"`.

## Turn in

- Files: `next_letter.py`
