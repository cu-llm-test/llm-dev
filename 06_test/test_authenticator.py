import pytest
from authenticator import Authenticator

def test_register_success(): # 1. register() でユーザーが正しく登録されるか
    # Arrange
    auth = Authenticator()

    # Act
    auth.register("user1", "pass1")

    # Assert
    assert "user1" in auth.users
    assert auth.users["user1"] == "pass1"

def test_register_duplicate_user(): # 2. register() で、既に存在するユーザー名で登録した場合にエラーになるか
    # Arrange
    auth = Authenticator()
    auth.register("user1", "pass1")

    # Act
    with pytest.raises(ValueError) as excinfo:
        auth.register("user1", "another_pass")

    # Assert
    assert str(excinfo.value) == "エラー: ユーザーは既に存在します。"

def test_login_success(): # 3. login() で、正しいユーザー名とパスワードでログインできるか
    # Arrange
    auth = Authenticator()
    auth.register("user1", "pass1")

    # Act
    message = auth.login("user1", "pass1")

    # Assert
    assert message == "ログイン成功"

def test_login_wrong_password(): # 4. login() で、誤ったパスワードの場合にエラーになるか
    # Arrange
    auth = Authenticator()
    auth.register("user1", "pass1")

    # Act
    with pytest.raises(ValueError) as excinfo:
        auth.login("user1", "wrong_pass")

    # Assert
    assert str(excinfo.value) == "エラー: ユーザー名またはパスワードが正しくありません。"
