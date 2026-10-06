import string

first = input()
second = input()
third = input()
shift = int(input())
alphabet = string.ascii_lowercase

a = (ord(first) - ord("a") + shift) % 26
b = (ord(second) - ord("a") + shift) % 26
c = (ord(third) - ord("a") + shift) % 26

print(chr(ord(alphabet[a])) + chr(ord(alphabet[b])) + chr(ord(alphabet[c])))
