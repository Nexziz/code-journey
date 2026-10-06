n = int(input())
for i in range(2 * n - 1):
    k = n - 1 - i
    if k < 0:
        k = -k
    d = n - 1 - k
    print(" " * k + chr(ord("a") + d) * (2 * d + 1))
