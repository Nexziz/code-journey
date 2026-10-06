# Ready, set, go

Level 1 · new skill: **output**

## Assignment

Print three lines. Every line ends with a newline:

    Ready
    Set
    Go!

## What you need to know

A `write` call sends exactly the bytes you ask for, nothing more. You can call it
once per line, or send several lines in one call by putting `\n` inside the text.

Count carefully: `"Ready\n"` is 6 bytes, because the newline is a byte too.
If you count too few, part of your text is cut off. Too many, and you send
garbage past the end of the text.

## Turn in

- Files: `countdown.c`
- Allowed functions: `write`
