
try:
    a = float(input("引数１:"))
    b = float(input("引数２:"))
except ValueError:
    # 数値以外が入力された場合
    print("エラー: 数値を入力してください")
finally:
    exit(1)

try:
    result = a / b
except ZeroDivisionError:
    # 数値以外が入力された場合
    print("エラー: 0で割ることはできません")
else:
    # 例外が発生しなかった場合
    print(f"計算結果: {result}")
