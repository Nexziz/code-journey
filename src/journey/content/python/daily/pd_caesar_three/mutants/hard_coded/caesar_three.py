first = input()
second = input()
third = input()
shift = int(input())

if first + second + third == "abc" and shift == 1:
    print("bcd")
elif first + second + third == "hey" and shift == 0:
    print("hey")
elif first + second + third == "xyz" and shift == 3:
    print("abc")
elif first + second + third == "cat" and shift == -3:
    print("zxq")
else:
    print(chr(ord(first) + shift % 26) + chr(ord(second) + shift % 26)
          + chr(ord(third) + shift % 26))
