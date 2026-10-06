# Boss: the staircase

Level 3 · boss

## Assignment

Print this staircase:

    a
    ab
    abc
    abcd
    abcde

## What you need to know

Row 1 has one letter, row 2 has two, and so on: a loop (the rows) containing
another loop (the letters). The inner loop runs completely every time the outer
loop goes round once:

    for row in range(1, 6):
        for col in range(row):
            ...
        ...

## Turn in

- Files: `staircase.py`
