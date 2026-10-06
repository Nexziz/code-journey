# Palindromes, properly

Daily · uses levels 1 to 5

## Assignment

Write a function in `is_palindrome.py`:

    def is_palindrome(text):

It returns `True` if the text reads the same forwards and backwards, **ignoring
case and every character that is not a letter or a digit**, and `False`
otherwise. The empty string is a palindrome.

## Things to think about

First build a cleaned-up version of the text: only the letters and digits, all
lowercase (`ch.isalnum()` tells you whether a character is a letter or digit, and
`ch.lower()` lowercases it). Then compare it with itself reversed. Slicing with a
negative step, `text[::-1]`, reverses a string or a list.

## Turn in

- Files: `is_palindrome.py`
