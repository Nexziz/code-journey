s = int(input())
hours = s // 3600
minutes = s // 60 % 60
seconds = s % 3600
print(f"{hours}:{minutes // 10}{minutes % 10}:{seconds // 10}{seconds % 10}")
