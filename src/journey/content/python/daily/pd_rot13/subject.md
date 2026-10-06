# Rot 13

## Assignment

Read one line and print it encoded with ROT13: every letter is replaced by the
letter 13 places further along the alphabet, wrapping around from `z` back to
`a`. Case is kept. Everything that is not a letter stays as it is.

    $ python3 rot13.py
    Hello, World!
    Uryyb, Jbeyq!

Do the work yourself: `codecs`, `str.translate` and `str.maketrans` are not
allowed.

## Turn in

- Files: `rot13.py`
