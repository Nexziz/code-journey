# Brainfuck interpreter

Weekly · uses levels 1 to 7 · about 3 hours

## Assignment

Write an interpreter for Brainfuck, a tiny language with eight commands. The
program to run is given as the **first and only argument**. If the program does
not receive exactly one argument, it prints only a newline.

The machine has a **tape** of 2048 cells, one byte each (`unsigned char`), all
starting at 0, and a **pointer** that starts at the first cell.

| command | meaning |
|---|---|
| `>` | move the pointer one cell to the right |
| `<` | move the pointer one cell to the left |
| `+` | add 1 to the current cell (255 + 1 wraps to 0) |
| `-` | subtract 1 from the current cell (0 - 1 wraps to 255) |
| `.` | write the current cell's byte to the terminal |
| `[` | if the current cell is 0, jump forward to just after the matching `]` |
| `]` | if the current cell is not 0, jump back to just after the matching `[` |

Every other character in the program is a comment and is ignored. There is no
input command to implement.

This program prints the letter `A` (8 * 8 + 1 = 65):

    $ ./brainfuck '++++++++[>++++++++<-]>+.'
    A

## What is new this week

Nothing in C: this week is about **planning**. You need an array for the tape,
pointers or indexes into both the tape and the program text, and nested loops
that find a bracket's partner. The partner search is the interesting part.
Counting depth works well: start at 1, step in the right direction, add 1 when
you see another bracket of the same kind, subtract 1 for the opposite kind, and
stop at 0.

## Things to think about

- Write the loop that walks through the program first, with only `+` and `.`.
  Then add commands one at a time and test after each.
- Run `./brainfuck` on hand-made programs, from tiny to the Hello World below.
- Programs in the tests never move the pointer outside the tape.

A famous program to try at the end:

    ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.

## Turn in

- Files: `brainfuck.c`
- Allowed functions: `write`
