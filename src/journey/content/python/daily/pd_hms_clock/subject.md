# Seconds on the clock

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

## Turn in

- Files: `hms_clock.py`
