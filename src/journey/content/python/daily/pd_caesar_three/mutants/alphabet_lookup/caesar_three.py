first = input()
second = input()
third = input()
shift = int(input())
alphabet = "abcdefghijklmnopqrstuvwxyz"

a = (alphabet.index(first) + shift) % 26
b = (alphabet.index(second) + shift) % 26
c = (alphabet.index(third) + shift) % 26

print(chr(ord(alphabet[a])) + chr(ord(alphabet[b])) + chr(ord(alphabet[c])))
