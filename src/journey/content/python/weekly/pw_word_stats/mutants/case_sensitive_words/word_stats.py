import sys

text = sys.stdin.read()
words = []
current = ""
for ch in text:
    if ch.isascii() and ch.isalpha():
        current += ch
    elif current:
        words.append(current)
        current = ""
if current:
    words.append(current)
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
ranking = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
print("lines", text.count("\n"))
print("words", len(words))
print("chars", len(text))
for word, count in ranking[:3]:
    print(word, count)
