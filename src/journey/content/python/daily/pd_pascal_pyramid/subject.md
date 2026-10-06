# Pascal's pyramid

## Assignment

Pascal's triangle starts with a single `1`. Every other number is the sum of the
two numbers just above it (a number missing at the edge counts as 0):

    1
    1 1
    1 2 1
    1 3 3 1
    1 4 6 4 1

Print its **first 10 rows** as a centred pyramid, with this exact layout:

- every number sits in a **cell 4 characters wide**, pushed to the right of the
  cell. With `_` standing for a space: `1` is `___1`, `10` is `__10` and `126`
  is `_126`;
- the cells of a row are glued together, with nothing in between;
- the first row is row 0. Row `r` is preceded by `2 * (9 - r)` spaces, so each row
  starts 2 spaces further left than the one below it, and the last row (row 9)
  gets none. In row 0 the `1` ends up with 18 + 3 = 21 spaces before it;
- no spaces at the end of a line, no blank lines.

The first four rows look like this:

    $ python3 pascal.py
                         1
                       1   1
                     1   2   1
                   1   3   3   1
    ...

Six more rows to go. Check them against the sum rule: every row reads the same
forwards and backwards, and the last row is 40 characters wide.

## Turn in

- Files: `pascal.py`
