class BankAccount:
    def __init__(self, initial_balance):
        self.__balance = initial_balance

    def deposit(self, amount):
        if amount < 0:
            print("エラー: 正しい金額を入力してください")
            return
        self.__balance += amount

    def withdraw(self, amount):
        """引き出し"""
        if amount <= 0 or amount > self.__balance:
            print("エラー: 残高不足または無効な金額です。")
            return
        self.__balance -= amount

    def get_balance(self):
        """現在の残高を返す"""
        return self.__balance


# 初期残高1000円でインスタンスを作成
account = BankAccount(1000)
# 500円を預け入れ
account.deposit(500)
# 200円を引き出し
account.withdraw(200)
# 現在の残高を表示（1300 と表示される）
print(account.get_balance())

# 1500円を引き出そうとする（エラー表示）
account.withdraw(1500)

# 無効な預け入れ
# account.deposit(-500)  
## エラー: 正しい金額を入力してください

# カプセル化
# print(account.__balance)
## AttributeError: 'BankAccount' object has no attribute '__balance'
# print(account._BankAccount__balance)
## 1300