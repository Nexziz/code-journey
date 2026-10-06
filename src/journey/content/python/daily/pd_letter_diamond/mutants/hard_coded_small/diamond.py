n = int(input())
if n == 1:
    print("a")
elif n == 2:
    print(" a")
    print("bbb")
    print(" a")
elif n == 3:
    print("  a")
    print(" bbb")
    print("ccccc")
    print(" bbb")
    print("  a")
elif n == 4:
    print("   a")
    print("  bbb")
    print(" ccccc")
    print("ddddddd")
    print(" ccccc")
    print("  bbb")
    print("   a")
elif n == 5:
    print("    a")
    print("   bbb")
    print("  ccccc")
    print(" ddddddd")
    print("eeeeeeeee")
    print(" ddddddd")
    print("  ccccc")
    print("   bbb")
    print("    a")
else:
    for i in range(n):
        print(" " * (n - 1 - i) + chr(ord("a") + i) * (2 * i + 1))
    for i in range(n - 2, -1, -1):
        print(" " * (n - 1 - i) + chr(ord("a") + i) * (2 * i))
