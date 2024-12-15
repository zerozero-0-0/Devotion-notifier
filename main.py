from datetime import datetime, timezone, timedelta
import os
import requests
from dotenv import load_dotenv
import discord
import asyncio
from zoneinfo import ZoneInfo

# 環境変数を読み込む
load_dotenv()
username = os.getenv("AtCoder_USERNAME")
discord_token = os.getenv("DISCORD_TOKEN")
discord_channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))

# discord clientの設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# メッセージを送信したい時間を設定
target_time_hour = 19
target_time_minute = 0

# チャンネルが非表示になることを妨げるためのメッセージを送信する時間を設定  
prevent_message_time_hour = 10
prevent_message_time_minute = 0

# タイムゾーンの設定
JST = ZoneInfo("Asia/Tokyo")

#エポック秒を取得する
# 今日の日付を取得
today = datetime.now(timezone.utc).date()

# 今日の午前0:00 UTCのdatetimeオブジェクトを作成
midnight_utc = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)

# エポック秒に変換
epoch_seconds = int(midnight_utc.timestamp())

url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={username}&from_second={epoch_seconds}"

async def fetch_data():
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
  return data

async def send_message(data, channel):
  if data is None:
    await channel.send("エラーが発生しました")
  elif len(data) == 0:
    await channel.send("今日はまだ提出していません")
      
async def prevent_channel_closed(channel):
    await channel.send("---このメッセージはチャンネルが非表示にならないようにするためのメッセージです。---\n")

@client.event
async def on_ready():
  channel = client.get_channel(discord_channel_id)
  if channel is None:
    print("指定されたチャンネルが見つかりません")
    return
  
  while not client.is_closed():
    now = datetime.now(JST)
    day = now.day
    target_time = now.replace(hour=target_time_hour, minute=target_time_minute)
    prevent_close_time = now.replace(hour=prevent_message_time_hour, minute=prevent_message_time_minute)

    if day % 4 == 0 :
      await prevent_channel_closed(channel)
      await asyncio.sleep(abs(target_time - prevent_close_time) * 60 * 60)
        
    if now > target_time:
      target_time += timedelta(days=1)
    
    wait_time = (target_time - now).total_seconds()
    
    await asyncio.sleep(wait_time)
      
    
    try:
      data = await fetch_data()
      await send_message(data)
      await prevent_channel_closed()

    except Exception as e:
      print(f"エラーが発生しました: {e}")
    
      if day % 4 == 3:
        await asyncio.sleep((24 + prevent_message_time_hour - target_time_hour) * 60 * 60)
      else:
        await asyncio.sleep(24 * 60 * 60)

client.run(discord_token)