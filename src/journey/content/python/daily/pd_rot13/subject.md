# Rot 13

Daily · uses levels 1 to 4

## Assignment

Read one line and print it encoded with ROT13: every letter is replaced by the
letter 13 places further along the alphabet, wrapping around from `z` back to
`a`. Case is kept. Everything that is not a letter stays as it is.

    $ python3 rot13.py
    Hello, World!
    Uryyb, Jbeyq!

Do the work yourself: `codecs`, `str.translate` and `str.maketrans` are not
allowed.

## Things to think about

There are 26 letters, so applying ROT13 twice gets the original text back. A
neat way to wrap around is `%`: think of a letter as a number from 0 to 25.
Build the result piece by piece: `result = result + new_char`.

## Turn in

- Files: `rot13.py`
