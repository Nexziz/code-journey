first = input()
second = input()
third = input()
shift = int(input())

a = (ord(first) - ord("a") + shift) % 26
b = (ord(second) - ord("a") + shift) % 26
c = (ord(third) - ord("a") + shift) % 26

print(chr(a + ord("a")))
print(chr(b + ord("a")))
print(chr(c + ord("a")))
