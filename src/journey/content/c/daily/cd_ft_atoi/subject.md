# Text to number

Daily · uses levels 1 to 6

## Assignment

Re-create `atoi`, which converts the number at the start of a string:

    int ft_atoi(char *str);

Rules:

1. skip the leading whitespace characters: space, `\t`, `\n`, `\v`, `\f`, `\r`
2. accept **one** optional sign, `+` or `-`
3. read digits for as long as there are digits; stop at the first other character
4. if there were no digits at all, the result is `0`

Inputs always fit in an `int`.

## Things to think about

Your function prints nothing. Beware of `-2147483648`: if you build the number
as a positive value first and negate it at the end, it overflows. Building it as
a negative value works for every `int`.

## Turn in

- Files: `ft_atoi.c`
- Allowed functions: none (`atoi` and friends are forbidden)
