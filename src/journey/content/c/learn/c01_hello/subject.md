# Hello, terminal

Level 1 · new skill: **output**

## Assignment

Write a program that prints exactly this line, followed by a newline:

    Hello, World!

## What you need to know

Every C program starts running at `main`. When `main` returns `0`, the program
tells the shell "everything went fine".

`write` sends bytes to a file descriptor. File descriptor `1` is the terminal
(standard output):

    write(1, "text", 4);    /* where to, the bytes, how many bytes */

The last number is how many bytes to send, so count the characters. `\n` is a
single character: the newline. You need `#include <unistd.h>` to use `write`.
Read more with `man 2 write`.

## Compile and run

    cc -Wall -Wextra -Werror hello.c -o hello
    ./hello

The grader compiles with exactly these flags, so a warning counts as an error.

## Turn in

- Files: `hello.c` (a starting skeleton is already in your folder)
- Allowed functions: `write`

Try it yourself first with `journey check`. When it passes, turn it in:
`git add . && git commit -m "hello" && git push`.
