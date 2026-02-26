# 必要なモジュールをインポート
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# ===== Stateクラスの定義 =====
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ===== グラフの構築 =====
def build_graph(model_name):
    # Web検索ツールの用意
    tools = [TavilySearchResults(max_results=3)]
    # LLM にツールをバインド
    model = ChatOpenAI(model=model_name).bind_tools(tools)

    # ワークフロー（グラフ）の定義
    workflow = StateGraph(State)

    # LLM を呼び出すノード
    def call_model(state: State):
        response = model.invoke(state["messages"])
        return {"messages": [response]}

    # ノードの追加
    workflow.add_node("model", call_model)
    workflow.add_node("tools", ToolNode(tools))

    # model ノードの出力に応じて、tools に進むか終了するかを分岐
    workflow.add_conditional_edges(
        "model",
        tools_condition,
        {"tools": "tools", "end": "__end__"},
    )

    # tools 実行後は再び model に戻る
    workflow.add_edge("tools", "model")

    # エントリーポイント
    workflow.set_entry_point("model")

    # メモリ（会話の継続用）
    memory = MemorySaver()

    # グラフをコンパイルして返す
    graph = workflow.compile(checkpointer=memory)
    return graph

# ===== グラフ実行関数 =====
def stream_graph_updates(graph: StateGraph, user_input: str):
    # 会話スレッドID（1つのチャットを通して同じIDを使う）
    config = {"configurable": {"thread_id": "thread-1"}}
    # 初期状態：ユーザー発話を messages に入れる
    inputs = {"messages": [("user", user_input)]}

    last_ai_message = None
    # 各ノードの更新を逐次取得
    for state in graph.stream(inputs, config, stream_mode="values"):
        messages = state["messages"]
        msg = messages[-1]
        # AI のメッセージだけを表示
        if getattr(msg, "type", None) == "ai":
            last_ai_message = msg

    if last_ai_message is not None:
        print(last_ai_message.content)

# ===== メイン実行ロジック =====
# 環境変数の読み込み
load_dotenv("../.env")
os.environ['OPENAI_API_KEY'] = os.environ['API_KEY']

# モデル名
MODEL_NAME = "gpt-4o-mini" 

# グラフの作成
graph = build_graph(MODEL_NAME)

# メインループ
print("こんにちは！(終了するときは空行を入力してください)")
while True:
    user_input = input()
    if user_input.strip() == "":
        break
    stream_graph_updates(graph, user_input)

print("ありがとうございました!")
