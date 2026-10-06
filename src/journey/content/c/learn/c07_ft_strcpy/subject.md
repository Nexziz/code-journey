# Copy a string

Level 7 · new skill: **pointers**

## Assignment

Re-create the standard `strcpy`:

    char *ft_strcpy(char *dest, char *src);

It copies the string `src`, **including its final `'\0'`**, into the memory that
`dest` points to, and returns `dest`.

## What you need to know

A `char *` is a pointer, and you can index a pointer like a row: `dest[i]`
reads or writes the i-th char after the address. The caller promises `dest` has
room for the whole string.

The test fills the destination with `Z` first: if you forget the `'\0'`, the
string will run on into those `Z`s and the test will show it.

## Turn in

- Files: `ft_strcpy.c`
- Allowed functions: none (`strcpy` itself is forbidden, of course)
