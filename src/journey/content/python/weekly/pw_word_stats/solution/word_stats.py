import sys


def find_words(text):
    words = []
    current = ""
    for ch in text:
        if ch.isascii() and ch.isalpha():
            current += ch.lower()
        elif current:
            words.append(current)
            current = ""
    if current:
        words.append(current)
    return words


def count_words(words):
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def main():
    text = sys.stdin.read()
    words = find_words(text)
    counts = count_words(words)
    ranking = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    print("lines", text.count("\n"))
    print("words", len(words))
    print("chars", len(text))
    for word, count in ranking[:3]:
        print(word, count)


main()
