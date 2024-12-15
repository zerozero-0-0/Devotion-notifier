# ベースイメージとしてPython 3.12を使用
FROM python:3.12-slim

WORKDIR /bot

# 必要なPythonパッケージをインストール
COPY requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY .  /bot

# ボットを実行
CMD python main.py