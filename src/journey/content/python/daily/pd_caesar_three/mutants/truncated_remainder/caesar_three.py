first = input()
second = input()
third = input()
shift = int(input())

a = ord(first) - ord("a") + shift
b = ord(second) - ord("a") + shift
c = ord(third) - ord("a") + shift

# a "C-style" remainder: the sign follows the number, so it can stay negative
if a >= 0:
    a = a % 26
else:
    a = -(-a % 26)
if b >= 0:
    b = b % 26
else:
    b = -(-b % 26)
if c >= 0:
    c = c % 26
else:
    c = -(-c % 26)

print(chr(a + ord("a")) + chr(b + ord("a")) + chr(c + ord("a")))
