for row in range(1, 6):
    for col in range(row):
        print(chr(ord("a") + col), end="")
    print()
