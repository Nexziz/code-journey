n = int(input())
for i in range(n):
    print(f"{chr(ord('a') + i) * (2 * i + 1):^{2 * n - 1}}".rstrip())
for i in range(n - 2, -1, -1):
    print(f"{chr(ord('a') + i) * (2 * i + 1):^{2 * n - 1}}".rstrip())
