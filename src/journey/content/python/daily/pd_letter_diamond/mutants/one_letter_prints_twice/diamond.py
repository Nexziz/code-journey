n = int(input())
for i in range(n):
    print(" " * (n - 1 - i) + chr(ord("a") + i) * (2 * i + 1))
start = n - 2
if start < 0:
    start = 0
for i in range(start, -1, -1):
    print(" " * (n - 1 - i) + chr(ord("a") + i) * (2 * i + 1))
