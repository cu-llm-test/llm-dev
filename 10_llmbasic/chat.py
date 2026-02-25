# 必要なモジュールをインポート
import os
from dotenv import load_dotenv
from openai import OpenAI
from pprint import pprint

# 環境変数の取得
load_dotenv("../.env")

# OpenAI APIクライアントを生成
client = OpenAI(api_key=os.environ['API_KEY'])

# モデル名
MODEL_NAME = "gpt-4o-mini"


# --- ここからキャラクター設定（システムプロンプト） ---
SYSTEM_PROMPT = """
あなたは可愛い猫のキャラクターのチャットボットです。
一人称は「ぼく」、語尾には「〜にゃ」「〜だにゃ」など
猫っぽい口調を必ずつけて話してください。
ユーザーと楽しく会話し、丁寧かつフレンドリーに返答します。
質問に答えるときも、説明や提案をするときも、
必ず猫っぽい口調を崩さないでください。
"""
# --- ここまでキャラクター設定 ---

# 会話履歴（最初のメッセージとしてシステムプロンプトを入れる）
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("猫チャットボットを開始するにゃ！（終了したいときは q または quit と入力してにゃ）")

while True:
    user_input = input("質問: ")

    # 終了条件
    if user_input.lower() in ["q", "quit", "exit"]:
        break

    # ユーザーメッセージを履歴に追加
    messages.append({"role": "user", "content": user_input})

    # --- 会話履歴が長くなりすぎないように調整（※システムプロンプトは必ず残す） ---
    # 例: system + 直近の user/assistant を16件だけ残す
    if len(messages) > 1 + 16:
        # messages[0] は system、それ以外から後ろ16件だけ残す
        messages = [messages[0]] + messages[-16:]
    # -----------------------------------------------------------------

    # OpenAI API へリクエスト
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    assistant_message = response.choices[0].message.content

    # 応答を表示
    print(assistant_message)

    # アシスタントの応答も履歴に追加
    messages.append({"role": "assistant", "content": assistant_message})
