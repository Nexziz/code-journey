from math import comb

for row in range(10):
    line = " " * (2 * (9 - row))
    for k in range(row + 1):
        line = line + str(comb(row, k)).rjust(4)
    print(line)
