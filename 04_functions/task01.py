def validate():
    i = input()
    if len(i) < 5 or len(i) > 15:
        print("ユーザー名は5文字以上15文字以内で入力してください")
        return False
    elif ' ' in i:
        print("ユーザー名に空白を含めることはできません")
        return False
    elif not(i.isalnum()):
        print("エラー: ユーザー名は英数字のみ使用できます")
        return False
    return True

if validate():
    print("ユーザー名は有効です")
else:
    print("不正なユーザー名です")