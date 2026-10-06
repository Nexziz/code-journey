# Boss: digit by digit

Level 2 · boss

## Assignment

Read a number between 1000 and 9999 and print its four digits separated by
dashes. Work it out with arithmetic: do not slice the text.

    $ python3 digits.py
    1728
    1-7-2-8

## What you need to know

You have the two tools: `//` cuts digits off the right, `%` keeps the right-hand
part.

    1728 // 1000         is 1
    1728 // 100 % 10     is 7

`print` can print several values at once. By default it puts a space between
them; `sep` changes that: `print(1, 2, 3, sep="-")` prints `1-2-3`.

## Turn in

- Files: `digits.py`
