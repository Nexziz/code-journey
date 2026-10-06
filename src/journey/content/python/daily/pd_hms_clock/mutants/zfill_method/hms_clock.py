s = int(input())
hours = s // 3600
minutes = str(s // 60 % 60).zfill(2)
seconds = str(s % 60).zfill(2)
print(f"{hours}:{minutes}:{seconds}")
