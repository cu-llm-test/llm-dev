# 必要なモジュールをインポート
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

# 環境変数の取得
load_dotenv("../.env")
os.environ['OPENAI_API_KEY']  = os.environ['API_KEY']

# モデル名
MODEL_NAME = "gpt-4o-mini"

# Indexの構築
documents = SimpleDirectoryReader('./data/text').load_data()
index = VectorStoreIndex.from_documents(documents)

# Chat Engineの作成
llm = OpenAI(model=MODEL_NAME)
chat_engine = index.as_chat_engine(llm=llm)

# チャットの開始
while(True):
    message = input("メッセージを入力:")
    if message.strip()=="":
        break
    display(f"質問:{message}")

    # 質問
    response = chat_engine.chat(message)

    # 回答を表示
    display(response.response)

print("\n---ご利用ありがとうございました！---")