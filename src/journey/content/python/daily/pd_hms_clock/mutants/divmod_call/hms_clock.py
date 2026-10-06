s = int(input())
minutes, seconds = divmod(s, 60)
hours, minutes = divmod(minutes, 60)
print(f"{hours}:{minutes // 10}{minutes % 10}:{seconds // 10}{seconds % 10}")
