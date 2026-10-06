s = int(input())
hours = s // 3600
minutes = s // 60 % 60
seconds = s % 60
print(f"{hours}:{minutes:02d}:{seconds:02d}")
