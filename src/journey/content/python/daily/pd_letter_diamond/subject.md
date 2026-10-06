# Letter diamond

Daily · uses levels 1 to 3

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

## Things to think about

This is the staircase boss, centred, with the letter changing from row to row.
The `i`-th letter is `chr(ord("a") + i)`. Text can be repeated with `*`
(`"-" * 9` is nine dashes), or you can print piece by piece with `end=""`.

The picture needs two stretches of rows: one that counts up, one that counts
down. `range` takes a third number, the step, so `range(5, 0, -1)` gives
5, 4, 3, 2, 1: mind where the counting stops. Which row comes right after the
widest one, and which row is the very last? The widest row must show up once.

Before you turn it in, run it for `n = 1` and `n = 2`: the shortest diamonds are
the ones that break first. To see stray spaces at the end of your lines, run
`python3 diamond.py | cat -A` (`cat -e` on a Mac): every line should end right
after its last letter, with a `$`. A last check: the diamond reads the same
upside down, and its widest row is `2 * n - 1` letters wide.

## Turn in

- Files: `diamond.py`
