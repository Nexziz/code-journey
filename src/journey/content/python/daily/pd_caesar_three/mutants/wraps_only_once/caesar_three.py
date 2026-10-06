first = input()
second = input()
third = input()
shift = int(input())

a = ord(first) - ord("a") + shift
b = ord(second) - ord("a") + shift
c = ord(third) - ord("a") + shift

if a > 25:
    a = a - 26
if a < 0:
    a = a + 26
if b > 25:
    b = b - 26
if b < 0:
    b = b + 26
if c > 25:
    c = c - 26
if c < 0:
    c = c + 26
weird = a % 26

print(chr(a + ord("a")) + chr(b + ord("a")) + chr(c + ord("a")))
