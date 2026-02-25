import statistics

grades = [85, 90, 78, 92, 88] 
mean = statistics.mean(grades)
max = max(grades)
min = min(grades)
ge_mean_number = len([x for x in grades if x >= mean])
print(f"平均点: {mean}")
print(f"最高点: {max}")
print(f"最低点: {min}")
print(f"平均以上の学生数: {ge_mean_number}")
