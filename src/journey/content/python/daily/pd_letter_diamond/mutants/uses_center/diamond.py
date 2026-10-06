n = int(input())
w = 2 * n - 1
for i in range(n):
    print((chr(ord("a") + i) * (2 * i + 1)).center(w).rstrip())
for i in range(n - 2, -1, -1):
    print((chr(ord("a") + i) * (2 * i + 1)).center(w).rstrip())
