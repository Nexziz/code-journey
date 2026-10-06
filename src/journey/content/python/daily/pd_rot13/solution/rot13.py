text = input()
result = ""
for ch in text:
    if "a" <= ch <= "z":
        result += chr((ord(ch) - ord("a") + 13) % 26 + ord("a"))
    elif "A" <= ch <= "Z":
        result += chr((ord(ch) - ord("A") + 13) % 26 + ord("A"))
    else:
        result += ch
print(result)
