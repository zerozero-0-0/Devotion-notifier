from datetime import datetime, timezone
import os
import requests
from dotenv import load_dotenv
import discord

# 環境変数を読み込む
load_dotenv()
username = os.getenv("AtCoder_USERNAME")

#エポック秒を取得する
# 今日の日付を取得
today = datetime.now(timezone.utc).date()

# 今日の午前0:00 UTCのdatetimeオブジェクトを作成
midnight_utc = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)

# エポック秒に変換
epoch_seconds = int(midnight_utc.timestamp())

url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={username}&from_second={epoch_seconds}"


try:
  response = requests.get(url)
  response.raise_for_status() #HTTPエラーチェック
  data = response.json()
except requests.exceptions.RequestException as e:
  print(f"HTTPリクエストエラー: {e}")
  data = None
except ValueError as e:
  print(f"JSONデコードエラー: {e}")
  data = None

if data is None:
  print("データの取得に失敗しました")
elif len(data) == 0:
    print("今日はまだ提出していません")
else:
  print("今日は提出しました")