# Letter diamond

## Assignment

Read one whole number `n`, from 1 to 26, and print a diamond made of the first
`n` letters of the alphabet.

The top half has `n` rows. Row number `i`, counting from 0, is made of the
`i`-th letter (`a` is letter 0, `b` is letter 1, and so on) repeated
`2 * i + 1` times, with `n - 1 - i` spaces in front of it. Each row is two
letters wider than the one before and starts one space further to the left.

The bottom half is the top half upside down, **without repeating the widest
row**. That makes `2 * n - 1` rows in all.

    $ python3 diamond.py
    3
      a
     bbb
    ccccc
     bbb
      a

    $ python3 diamond.py
    2
     a
    bbb
     a

    $ python3 diamond.py
    1
    a

The spaces go in front of the letters only: a line must end right after its last
letter, and the program ends with a newline as usual.

You may not call `.center`, `.ljust` or `.rjust`, align text inside an f-string
(`{x:^9}`), or `import string`. Typing the alphabet by hand is not allowed
either. The grader checks all of this: count the spaces yourself, and get the
letters from `chr` and `ord`.

## Turn in

- Files: `diamond.py`
