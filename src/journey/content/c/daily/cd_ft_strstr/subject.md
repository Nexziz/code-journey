# Find a word

Daily · uses levels 1 to 7

## Assignment

Re-create `strstr`:

    char *ft_strstr(char *str, char *to_find);

Return a pointer to the **first** occurrence of `to_find` inside `str`, or `0`
(a null pointer) if it does not occur. An empty `to_find` is found at the start:
return `str`.

## Things to think about

A pointer into the middle of a string is just `str + i` (or `&str[i]`). Try each
start position in turn, and for each one compare as long as the characters match.
A comparison that fails half-way means "try the next start position", not
"give up". Memory is checked: never read beyond the `'\0'` of either string.

## Turn in

- Files: `ft_strstr.c`
- Allowed functions: none
