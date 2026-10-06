s = int(input())
hours = int(s * 0.00027778)
minutes = s // 60 % 60
seconds = s % 60
print(f"{hours}:{minutes // 10}{minutes % 10}:{seconds // 10}{seconds % 10}")
