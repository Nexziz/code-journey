s = int(input())
hours = s // 3600
minutes = ("0" + str(s // 60 % 60))[-2:]
seconds = ("0" + str(s % 60))[-2:]
print(f"{hours}:{minutes}:{seconds}")
