import time

s = int(input())
print(time.strftime("%H:%M:%S", time.gmtime(s)))
