n = int(input())
letters = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
for i in range(n):
    print(" " * (n - 1 - i) + letters[i] * (2 * i + 1))
for i in range(n - 2, -1, -1):
    print(" " * (n - 1 - i) + letters[i] * (2 * i + 1))
