# Word count

## Assignment

Write your own `wc`. The program reads everything from its **standard input**
until the input ends, then prints three numbers separated by single spaces and
followed by a newline:

    lines words characters

- **lines**: how many `\n` characters the input contains
- **words**: how many separate words, where a word is a run of characters that
  are not whitespace (space, `\t`, `\n`, `\v`, `\f`, `\r`)
- **characters**: how many bytes the input has


    $ printf 'hello world\n' | ./wc
    1 2 12
    $ ./wc < /dev/null
    0 0 0

Limit: the input can be several hundred kilobytes.

## Turn in

- Files: `wc.c`
- Allowed functions: `read`, `write`
