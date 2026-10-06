# Text report

## Assignment

Write a program that reads all of its standard input and prints a small report:

    lines <number of lines>
    words <number of words>
    chars <number of characters>
    <word> <count>
    <word> <count>
    <word> <count>

- **lines** is how many newline characters the text contains
- a **word** is a maximal run of English letters (`a` to `z`, either case). Every
  other character, digits and punctuation included, separates words. Words are
  compared in lowercase: `The` and `the` are the same word
- **chars** is the total number of characters
- then come the three most frequent words, most frequent first. Words with the
  same count are sorted alphabetically. If there are fewer than three different
  words, print fewer lines

For this input

    The cat saw the dog. The dog ran!

the report is

    lines 1
    words 8
    chars 34
    the 3
    dog 2
    cat 1

## Turn in

- Files: `word_stats.py`
