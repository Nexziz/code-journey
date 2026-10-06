# Word count

Weekly · uses levels 1 to 7 · about 2 to 3 hours

## Assignment

Write your own `wc`. The program reads everything from its **standard input**
until the input ends, then prints three numbers separated by single spaces and
followed by a newline:

    lines words characters

- **lines**: how many `\n` characters the input contains
- **words**: how many separate words, where a word is a run of characters that
  are not whitespace (space, `\t`, `\n`, `\v`, `\f`, `\r`)
- **characters**: how many bytes the input has

<br>

    $ printf 'hello world\n' | ./wc
    1 2 12
    $ ./wc < /dev/null
    0 0 0

## What is new this week

Reading input. `read` is the mirror image of `write`:

    ssize_t read(int fd, void *buf, size_t count);

- file descriptor `0` is the keyboard, or whatever has been piped in
- it stores up to `count` bytes into `buf` and returns how many it stored
- it returns `0` when the input is over, and `-1` on an error
- it often returns **less** than you asked for, so call it in a loop

A buffer is simply an array: `char buf[4096];` is 4096 chars in a row, and
`sizeof(buf)` is 4096.

Test it by hand with a pipe (`printf 'a b\n' | ./wc`), a file (`./wc < wc.c`)
and the real thing (`wc < wc.c`) to compare.

## Things to think about

- Process the input chunk by chunk. What if a word is cut in half between two
  calls to `read`? You will need a variable that remembers "was the previous
  character part of a word?".
- The counts can be large, so print numbers with your own routine, like the
  boss of level 5. `long` is a bigger integer type if you want extra room.
- Plan before you type: three counters, one flag, one loop inside one loop.

## Turn in

- Files: `wc.c`
- Allowed functions: `read`, `write`
