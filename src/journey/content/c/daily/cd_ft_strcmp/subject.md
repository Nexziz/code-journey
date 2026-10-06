# Compare two strings

Daily · uses levels 1 to 7

## Assignment

Re-create `strcmp`:

    int ft_strcmp(char *s1, char *s2);

Compare the strings character by character. Return a negative number if `s1`
comes before `s2`, `0` if they are equal and a positive number if `s1` comes
after `s2`. The classic result is the difference between the first two
characters that differ.

## Things to think about

The end marker `'\0'` takes part in the comparison: that is how `"ab"` ends up
smaller than `"abc"`. Characters are compared as **unsigned** values (0 to 255),
so cast to `unsigned char` before subtracting.

## Turn in

- Files: `ft_strcmp.c`
- Allowed functions: none
