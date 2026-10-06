for i in range(26):
    letter = chr(ord("a") + i)
    if letter in "aeiou":
        letter = letter.upper()
    print(letter, end="")
print()
