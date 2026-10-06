# A program that prints a program

Daily · uses levels 1 to 1

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

## Things to think about

Quotes and backslashes need a little care inside Python text. This is the one
new tool of the task:

- A quote of the *other* kind needs no help: `"it's"` and `'say "hi"'` are fine
  as they are.
- To put a quote of the *same* kind inside, put a backslash in front of it: `\"`
  inside `"..."`, `\'` inside `'...'`.
- A backslash starts a special code, so to get one backslash you write two:
  `\\` shows a single `\`.
- `\n` is a line break and `\t` is a tab. To show a backslash followed by the
  letter n, write `\\n`.

A few examples:

    print("say \"hi\"")     shows   say "hi"
    print('C:\\temp')       shows   C:\temp
    print("a\nb")           shows   a   and then b on the next line
    print("a\\nb")          shows   a\nb   (one line)

Your seven lines mix both quote styles, so choose for each line the quote style
that needs the fewest escapes. Work one line at a time: print the first line,
run it, then add the next. If you like, a raw string `r"..."` (backslashes are
not special inside it) or a triple-quoted string `"""..."""` (it may hold both
kinds of quote and line breaks) can make some lines easier, but plain escapes
are enough.

A good way to check your work: save what your program prints in a file and run
that file. It should show the six lines of the comparison above.

    python3 print_source.py > greet.py
    python3 greet.py

Watch the details: there is no space at the end of any line, `print` already
ends each line, and the last line ends with two backslashes, a double quote and
a closing parenthesis.

Only `print` is needed here. Do not read the text from somewhere else and do not
build it with `chr()` or `ord()`: `import`, `open`, `input`, `exec`, `eval`,
`chr` and `ord` are not allowed.

## Turn in

- Files: `print_source.py`
