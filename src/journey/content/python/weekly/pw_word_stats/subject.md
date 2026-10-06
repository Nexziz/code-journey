# Text report

Weekly · uses levels 1 to 5 · about 2 to 3 hours

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

## What is new this week

- Reading everything at once: `import sys` and then `text = sys.stdin.read()`.
- **Dictionaries** map keys to values, which is exactly what counting words needs:

      counts = {}
      counts["cat"] = 1
      counts["cat"] = counts.get("cat", 0) + 1   # get() gives 0 if the key is missing

  `counts.items()` gives the key/value pairs.
- Sorting with a rule: `sorted(items, key=...)` where the key can be a tuple.
  Python sorts tuples element by element, and a minus sign flips a number's order:
  `key=lambda item: (-item[1], item[0])` sorts by count descending, then by word.
  (`lambda` is just a tiny unnamed function.)

## Things to think about

- Split the work into functions: one that finds the words, one that counts them,
  one that prints. You can test each of them separately with a few lines of text.
- Walk through the text one character at a time, building up the current word.
  `ch.isalpha()` tells you whether a character is a letter, but be careful: it is
  true for accented letters too, so also check `ch.isascii()`.
- Try your program on its own source: `python3 word_stats.py < word_stats.py`.

## Turn in

- Files: `word_stats.py`
