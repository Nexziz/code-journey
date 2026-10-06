# Swap two values

Level 7 · new skill: **pointers**

## Assignment

Write a function that swaps the values of two integers that belong to its
caller:

    void ft_swap(int *a, int *b);

## What you need to know

A function only gets *copies* of its arguments, so it cannot change the caller's
variables... unless it is told **where they live**. That is a pointer: a
variable that holds an address.

    int x = 5;
    int *p = &x;        /* p holds the address of x */
    *p = 9;             /* follow the address and store 9: x is now 9 */

- `&x` means "the address of x"
- `int *p` declares a pointer to an int
- `*p` means "the int at that address", to read it or to write it

The caller writes `ft_swap(&a, &b)` and your function receives the two
addresses. You have already used `&` with `write(1, &c, 1)`.

## Turn in

- Files: `ft_swap.c`
- Allowed functions: none
