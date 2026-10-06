first = input()
second = input()
third = input()
shift = int(input())

a = (ord(first) - ord("a") + shift) % 26
b = (ord(second) - ord("a") + shift) % 26
c = (ord(third) - ord("a") + shift) % 26

print(chr(c + ord("a")) + chr(b + ord("a")) + chr(a + ord("a")))
