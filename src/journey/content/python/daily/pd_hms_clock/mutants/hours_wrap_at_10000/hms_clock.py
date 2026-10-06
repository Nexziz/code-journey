s = int(input())
hours = s // 3600 % 10000
minutes = s // 60 % 60
seconds = s % 60
print(f"{hours}:{minutes // 10}{minutes % 10}:{seconds // 10}{seconds % 10}")
