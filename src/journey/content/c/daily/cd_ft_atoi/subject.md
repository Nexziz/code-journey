# Text to number

## Assignment

Re-create `atoi`, which converts the number at the start of a string:

    int ft_atoi(char *str);

Rules:

1. skip the leading whitespace characters: space, `\t`, `\n`, `\v`, `\f`, `\r`
2. accept **one** optional sign, `+` or `-`
3. read digits for as long as there are digits; stop at the first other character
4. if there were no digits at all, the result is `0`

Inputs always fit in an `int`.

## Turn in

- Files: `ft_atoi.c`
- Allowed functions: none (`atoi` and friends are forbidden)
- No `main`: a test program calls your function.
