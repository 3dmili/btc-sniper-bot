import requests
import pandas as pd
from datetime import datetime, timedelta

# === CONFIG ===
symbol = "BTCUSDT"
interval = "5m"
limit = 300  # ~25 hours worth of candles

url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
response = requests.get(url)
data = response.json()

# === CREATE DATAFRAME ===
df = pd.DataFrame(data, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "trades", "taker_buy_base",
    "taker_buy_quote", "ignore"
])

df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)

# === EXTRACT YESTERDAY’S SESSION ===
now = datetime.utcnow()
yesterday = now - timedelta(days=1)
today = now.date()
yesterday_start = datetime.combine(today - timedelta(days=1), datetime.min.time())
yesterday_end = datetime.combine(today - timedelta(days=1), datetime.max.time())

df_yesterday = df[(df["timestamp"] >= yesterday_start) & (df["timestamp"] <= yesterday_end)]

box_high = df_yesterday["high"].max()
box_low = df_yesterday["low"].min()

# === CALCULATE EMA-50 & RSI ===
df["ema50"] = df["close"].ewm(span=50).mean()

delta = df["close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
df["rsi"] = 100 - (100 / (1 + rs))

# === GET LAST CANDLE ===
last = df.iloc[-1]
price = last["close"]
ema = last["ema50"]
rsi = last["rsi"]

# === BOX & SIGNAL CHECK ===
print(f"🟦 Yesterday's Box: HIGH = {box_high:.2f}, LOW = {box_low:.2f}")
print(f"📍 Current Price: {price:.2f}")
print(f"📊 EMA-50: {ema:.2f}, RSI: {rsi:.2f}")

# === FINAL DECISION ===
if price > box_high and price > ema and rsi > 50:
    print("🔼 BUY SIGNAL: Broke above box + above EMA + RSI strong")
elif price < box_low and price < ema and rsi < 50:
    print("🔽 SELL SIGNAL: Broke below box + below EMA + RSI weak")
else:
    print("⏸ WAIT: No clean break or mixed signal")
