# Echo the arguments

Level 6 · new skill: **strings**

## Assignment

Write a program that prints every argument it receives, one per line, in order.
Do not print the program's own name. With no arguments it prints nothing.

    $ ./echo one two three
    one
    two
    three

## What you need to know

`main` can receive the command line:

    int main(int argc, char **argv)

- `argc` is how many words were typed, **including the program's name**
- `argv[0]` is the program's name, `argv[1]` the first real argument, and so on
- each `argv[i]` is a string, so everything you learned above applies

Running `./echo one two three` gives `argc == 4`.

## Turn in

- Files: `print_params.c`
- Allowed functions: `write`
