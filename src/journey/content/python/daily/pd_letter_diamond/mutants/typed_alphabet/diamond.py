n = int(input())
letters = "abcdefghijklmnopqrstuvwxyz"
for i in range(n):
    print(" " * (n - 1 - i) + letters[i] * (2 * i + 1))
for i in range(n - 2, -1, -1):
    print(" " * (n - 1 - i) + letters[i] * (2 * i + 1))
