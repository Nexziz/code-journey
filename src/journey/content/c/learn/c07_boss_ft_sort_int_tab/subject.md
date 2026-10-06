# Boss: sort an array

Level 7 · boss

## Assignment

Write a function that sorts an array of integers in ascending order, in place:

    void ft_sort_int_tab(int *tab, int size);

`tab` points at the first of `size` integers. `size` can be 0.

## What you need to know

A pointer to an int can be indexed like an array: `tab[0]`, `tab[1]`, ...
`tab[size - 1]`. Writing to `tab[i]` changes the caller's array.

Pick any simple sorting method you can reason about, for example: repeatedly
walk through the array and swap neighbours that are in the wrong order, until
a full pass swaps nothing. The grader checks memory: touching `tab[size]` or
`tab[-1]` is an error.

## Turn in

- Files: `ft_sort_int_tab.c`
- Allowed functions: none
