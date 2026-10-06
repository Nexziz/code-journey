text = input()
result = ""
for ch in text:
    if ch.isalpha():
        result += chr(ord(ch) + 13)
    else:
        result += ch
print(result)
