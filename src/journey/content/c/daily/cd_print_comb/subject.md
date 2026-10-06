# Every combination

Daily · uses levels 1 to 4

## Assignment

Print every combination of three **different** digits in ascending order, as
three-digit groups separated by a comma and a space, on a single line:

    012, 013, 014, 015, 016, 017, 018, 019, 023, ..., 689, 789

`012` is valid, `021` is not (the digits must increase), and neither is `011`.
There is no comma after the last combination, and the line ends with a newline.

## Things to think about

Three nested loops, where each loop starts just above the previous digit. The
hard part is the separator: the very last combination must not be followed by
`, `. How can the program recognise it?

## Turn in

- Files: `print_comb.c`
- Allowed functions: `write`
