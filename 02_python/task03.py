capital = int(input("元金を入力してください:"))
interest = int(input("年利を入力してください:")) / 100
acc = capital
for _ in range(10):
    acc = acc * (1 + interest)

print(f"10年後の金額:{acc:.2f}")
