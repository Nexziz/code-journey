import string

n = int(input())
for i in range(n):
    print(" " * (n - 1 - i) + chr(ord(string.ascii_lowercase[0]) + i) * (2 * i + 1))
for i in range(n - 2, -1, -1):
    print(" " * (n - 1 - i) + chr(ord(string.ascii_lowercase[0]) + i) * (2 * i + 1))
