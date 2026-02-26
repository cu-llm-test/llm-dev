# 必要なモジュールをインポート
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam
from tavily import TavilyClient

# 環境変数の取得
load_dotenv("../.env")

# OpenAI APIクライアントを生成
client = OpenAI(api_key=os.environ['API_KEY'])

# tavily検索用APIキーの取得
TAVILY_API_KEY = os.environ['TAVILY_API_KEY']

# モデル名
MODEL_NAME = "gpt-4o-mini"

def get_search_result(question):
    client = TavilyClient(api_key=TAVILY_API_KEY)
    response = client.search(question)
    return json.dumps({"result": response["results"]})

    # テスト用コード
ret = get_search_result("東京駅のイベントを教えて")
json.loads(ret)

# ツール定義
def define_tools():
    print("------define_tools(ツール定義)------")
    return [
        ChatCompletionToolParam({
            "type": "function",
            "function": {
                "name": "get_search_result",
                "description": "最近一ヵ月のイベント開催予定などネット検索が必要な場合に、質問文の検索結果を取得する",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "質問文"},
                    },
                    "required": ["question"],
                },
            },
        })
    ]

    # 言語モデルへの質問を行う関数
def ask_question(question, tools):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": question}],
        tools=tools,
        tool_choice="auto",
    )
    return response

# ツール呼び出しが必要な場合の処理を行う関数
def handle_tool_call(response, question):
    # 関数の実行と結果取得
    tool = response.choices[0].message.tool_calls[0]
    function_name = tool.function.name
    arguments = json.loads(tool.function.arguments)
    function_response = globals()[function_name](**arguments)

    # 関数の実行結果をmessagesに加えて再度言語モデルを呼出
    response_after_tool_call = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": question},
            response.choices[0].message,
            {
                "tool_call_id": tool.id,
                "role": "tool",
                "content": function_response,
            },
        ],
    )
    return response_after_tool_call


# ユーザーからの質問を処理する関数
def process_response(question, tools):
    response = ask_question(question, tools)

    if response.choices[0].finish_reason == 'tool_calls':
        # ツール呼出の場合
        final_response = handle_tool_call(response, question)
        return final_response.choices[0].message.content.strip()
    else:
        # 言語モデルが直接回答する場合
        return response.choices[0].message.content.strip()

tools = define_tools()

# 言語モデルが直接回答できる質問
question = "東京都と沖縄県はどちらが広いですか？"
response_message = process_response(question, tools)
print(response_message)


tools = define_tools()

# ツール呼出が必要な質問
question = "東京駅のイベントについて、最近1ヶ月以内の検索結果を教えてください"
response_message = process_response(question, tools)
print(response_message)


# チャットボットへの組み込み
tools = define_tools()

messages=[]

while(True):
    # ユーザーからの質問を受付
    question = input("メッセージを入力:")
    # 質問が入力されなければ終了
    if question.strip()=="":
        break
    display(f"質問:{question}")

    # メッセージにユーザーからの質問を追加
    messages.append({"role": "user", "content": question.strip()})
    # やりとりが8を超えたら古いメッセージから削除
    if len(messages) > 8:
        del_message = messages.pop(0)

    # 言語モデルに質問
    response_message = process_response(question, tools)

    # メッセージに言語モデルからの回答を追加
    print(response_message, flush=True)
    messages.append({"role": "assistant", "content": response_message})

print("\n---ご利用ありがとうございました！---")