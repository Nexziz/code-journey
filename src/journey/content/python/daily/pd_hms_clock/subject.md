# Seconds on the clock

Daily · uses levels 1 to 2

## Assignment

Read one whole number `s` between 0 and 99999999: a number of seconds. Print it
as a clock reading `H:MM:SS`, so hours, minutes and seconds with a colon between
them.

- The **hours** are written plainly. No leading zero, and they never wrap around
  at 24: 100 hours is `100:00:00`. With such large inputs the hours field can
  have anything from 1 to 5 digits.
- The **minutes** and the **seconds** always have two digits, so five seconds is
  `05`, not `5`. Each of them is always below 60.

For example:

    $ python3 hms_clock.py
    3725
    1:02:05

    $ python3 hms_clock.py
    1000000
    277:46:40

Zero seconds is `0:00:00`: the hours stay a single `0`, the other two fields
are padded.

## Things to think about

An hour is 3600 seconds and a minute is 60. Take 3725 seconds by hand:

- the hours are how many whole hours fit in it: `3725 // 3600` is 1
- the seconds are what is left after whole minutes: `3725 % 60` is 5
- `3725 // 60` is 62, the minutes since the start. Only the part past a whole
  hour belongs in the minutes field, so wrap it at 60 with `%`

An f-string puts values into text. Anything between the braces is calculated
first: with `h = 7`, `f"{h}:30"` is `7:30` and `f"{h * 2}"` is `14`.

Padding is the twist. The usual tools for it (format specs like `:02d`,
`zfill`, `rjust`, `format`) are not allowed, and neither are `divmod`, slicing
text, or the `time` and `datetime` modules. But a two-digit field is just two
digits: for a number `x` below 100 the tens digit is `x // 10` and the ones
digit is `x % 10`. Print them side by side, with nothing in between, and you
get `05` for 5 and `42` for 42, without an `if`.

Before you turn it in, try 0, 59, 60, 3599, 3600, 86400 and 99999999.

## Turn in

- Files: `hms_clock.py`
