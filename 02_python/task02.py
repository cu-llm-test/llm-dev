price_ex = int(input("税抜価格を入力してください（円）："))
price_incl = int(price_ex * (1 + 0.1))

if price_incl >= 2000:
    shipping = 0
else:
    shipping = 350

total_price = price_incl + shipping
shipping_str = "無料" if shipping == 0 else f"{shipping}円"
print(f"送料は{shipping_str}です")
print(f"送料込価格は{total_price}円です")