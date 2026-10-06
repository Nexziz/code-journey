# A program that prints a program

## Assignment

Write a program that prints these seven lines, exactly as shown:

    # greet.py
    name = "World"
    print("Hello, \"" + name + "\"!")
    print('It\'s here: C:\\new\\table')
    print("line one\nline two")
    print('say "cheese"')
    print("it's a backslash: \\")

The text happens to be a tiny Python script, so it is full of quotes and
backslashes. Your program does not *run* that script, it only *shows* it: every
quote, every backslash and every letter has to come out exactly where it is
above.

For comparison, if you saved those seven lines as `greet.py` and ran it, you
would see this (this is **not** what your program prints):

    Hello, "World"!
    It's here: C:\new\table
    line one
    line two
    say "cheese"
    it's a backslash: \

## Turn in

- Files: `print_source.py`
