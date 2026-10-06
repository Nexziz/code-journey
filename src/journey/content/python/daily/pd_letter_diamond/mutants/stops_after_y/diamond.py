n = int(input())
for i in range(n):
    letter = chr(ord("a") + i % 25)
    print(" " * (n - 1 - i) + letter * (2 * i + 1))
for i in range(n - 2, -1, -1):
    letter = chr(ord("a") + i % 25)
    print(" " * (n - 1 - i) + letter * (2 * i + 1))
