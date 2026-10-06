# Division and remainder

Level 7 · new skill: **pointers**

## Assignment

Write a function that computes both the quotient and the remainder of `a / b`
and hands them back through pointers:

    void ft_div_mod(int a, int b, int *div, int *mod);

After the call, `*div` holds `a / b` and `*mod` holds `a % b`. The inputs are
never zero for `b`.

## What you need to know

A function can only `return` one value. To hand back two, the caller gives you
the addresses of two variables and you write the results into them with `*div =
...` and `*mod = ...`.

## Turn in

- Files: `ft_div_mod.c`
- Allowed functions: none
