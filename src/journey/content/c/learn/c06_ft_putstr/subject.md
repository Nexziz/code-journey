# Print a string

Level 6 · new skill: **strings**

## Assignment

Write a function that prints a string, without a newline:

    void ft_putstr(char *str);

## What you need to know

You can write the string one character at a time, or measure it first (like in
the last exercise) and send it with a single `write(1, str, length)`. Both are
fine. Remember to stop at `'\0'`, and never print the `'\0'` itself.

## Turn in

- Files: `ft_putstr.c`
- Allowed functions: `write`
