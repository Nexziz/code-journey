import sys

text = sys.stdin.read()
words = text.lower().split()
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
ranking = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
print("lines", text.count("\n"))
print("words", len(words))
print("chars", len(text))
for word, count in ranking[:3]:
    print(word, count)
