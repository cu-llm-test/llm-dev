# README.md

## 初期環境構築
```python
# 仮想化環境
python3.11 -m venv .venv311
source .venv311/bin/activate
# パッケージインストール
python -m pip install --upgrade pip
pip install "langchain>=0.1.0,<0.2.0" --upgrade
pip install llama-index openai python-dotenv ipykernel jupyter langgraph langchain-chroma langchain-openai langchain-community flask
# Jupyter カーネル
python -m ipykernel install --user --name llm-venv --display-name "Python (llm-venv3.11)"
```