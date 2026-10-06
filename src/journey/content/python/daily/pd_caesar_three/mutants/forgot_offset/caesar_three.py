first = input()
second = input()
third = input()
shift = int(input())

a = (ord(first) + shift) % 26
b = (ord(second) + shift) % 26
c = (ord(third) + shift) % 26

print(chr(a + ord("a")) + chr(b + ord("a")) + chr(c + ord("a")))
