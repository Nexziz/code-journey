# Reverse an array

Daily · uses levels 1 to 7

## Assignment

Write a function that reverses an array of integers in place:

    void ft_rev_int_tab(int *tab, int size);

`{1, 2, 3, 4, 5}` becomes `{5, 4, 3, 2, 1}`. `size` can be 0.

## Things to think about

You only need to walk through half of the array, swapping the element at each end
with the one at the other end. Do not walk through the whole thing, or you will
swap everything back again. Memory is checked: stay inside `tab[0]` ...
`tab[size - 1]`.

## Turn in

- Files: `ft_rev_int_tab.c`
- Allowed functions: none
