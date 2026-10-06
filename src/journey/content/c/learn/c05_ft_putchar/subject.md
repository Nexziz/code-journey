# Your own putchar

Level 5 · new skill: **functions**

## Assignment

Write a function that prints one character:

    void ft_putchar(char c);

It prints `c` and nothing else: no newline.

## What you need to know

Until now everything lived inside `main`. A function is a named piece of code you
can call whenever you like:

    void say_hi(void)           /* gives back nothing, takes nothing */
    {
        write(1, "hi\n", 3);
    }

    int add(int a, int b)       /* takes two ints, gives back an int */
    {
        return (a + b);
    }

`void` as a return type means "gives back nothing". The parameters `a` and `b`
are variables that receive the values you pass: `add(2, 3)` runs with `a` equal
to 2 and `b` equal to 3. `return` hands a value back to the caller.

From now on exercises ask for **a function in a file**, not a whole program.
Your file has no `main`: the grader brings its own `main` that calls your
function with different inputs. Do not write one.

## Turn in

- Files: `ft_putchar.c`
- Allowed functions: `write`
