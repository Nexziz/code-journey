# Measure a string

Level 6 · new skill: **strings**

## Assignment

Write a function that returns the length of a string, not counting the end
marker:

    int ft_strlen(char *str);

## What you need to know

A string is a row of chars in memory that ends with a special char, `'\0'` (the
number 0). `"hi"` takes 3 bytes: `'h'`, `'i'` and `'\0'`.

A function receives a string as `char *str`. For now read that as "the address
of the first character". You index it like a row: `str[0]` is the first char,
`str[1]` the next, and so on, until you reach `'\0'`.

This counts the letter `a` in a string:

    int count_a(char *str)
    {
        int i;
        int n;

        i = 0;
        n = 0;
        while (str[i] != '\0')
        {
            if (str[i] == 'a')
                n++;
            i++;
        }
        return (n);
    }

Never read past the `'\0'`: the grader runs your code with memory checks.

## Turn in

- Files: `ft_strlen.c`
- Allowed functions: none (`strlen` itself is of course forbidden)
