# Boss: the staircase

Level 3 · boss

## Assignment

Print this staircase. Every row ends with a newline:

    a
    ab
    abc
    abcd
    abcde

## What you need to know

Row 1 has one letter, row 2 has two, and so on. That is a loop (the rows)
containing another loop (the letters). The inner loop runs completely every
time the outer loop goes round once:

    for (row = 1; row <= 5; row++)
    {
        for (col = 0; col < row; col++)
            ...
        ...
    }

## Turn in

- Files: `staircase.c`
- Allowed functions: `write`
