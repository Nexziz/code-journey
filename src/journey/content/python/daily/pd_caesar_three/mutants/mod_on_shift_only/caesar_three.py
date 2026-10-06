first = input()
second = input()
third = input()
shift = int(input()) % 26

print(chr(ord(first) + shift) + chr(ord(second) + shift) + chr(ord(third) + shift))
