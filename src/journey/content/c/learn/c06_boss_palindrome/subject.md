# Boss: palindromes

Level 6 · boss

## Assignment

Write a program that checks whether its argument reads the same forwards and
backwards.

- given exactly one argument: print `yes` or `no`, then a newline
- given any other number of arguments: print only a newline

    $ ./palindrome level
    yes
    $ ./palindrome journey
    no

The comparison is case-sensitive, and the empty string counts as a palindrome.

## What you need to know

Everything from levels 1 to 6. A good plan: find the length of the string, then
compare the first character with the last, the second with the second to last,
and so on, until the two positions meet.

## Turn in

- Files: `palindrome.c`
- Allowed functions: `write`
