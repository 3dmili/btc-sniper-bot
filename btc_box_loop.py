import time
from datetime import datetime, timedelta
import requests
import pandas as pd

SYMBOL = "BTCUSDT"
INTERVAL = "5m"
LIMIT = 300  # number of candles (~25 hours)
URL = f"https://api.binance.com/api/v3/klines"


def fetch_candles(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
    return df


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ema50"] = df["close"].ewm(span=50).mean()
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df


def yesterday_box(df: pd.DataFrame) -> tuple[float, float]:
    now = datetime.utcnow()
    yesterday_date = now.date() - timedelta(days=1)
    start = datetime.combine(yesterday_date, datetime.min.time())
    end = datetime.combine(yesterday_date, datetime.max.time())
    df_yesterday = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    if df_yesterday.empty:
        return float('nan'), float('nan')
    return df_yesterday["high"].max(), df_yesterday["low"].min()


def check_signal(df: pd.DataFrame, box_high: float) -> None:
    last = df.iloc[-1]
    price = last["close"]
    ema = last["ema50"]
    rsi = last["rsi"]
    print(f"🟦 Yesterday's Box: HIGH = {box_high:.2f}")
    print(f"📍 Current Price: {price:.2f}")
    print(f"📊 EMA-50: {ema:.2f}, RSI: {rsi:.2f}")
    if price > box_high and price > ema and rsi > 60:
        print("🔼 BUY SIGNAL")
    else:
        print("⏸ WAIT")


def main():
    while True:
        try:
            df = fetch_candles(SYMBOL, INTERVAL, LIMIT)
            df = calculate_indicators(df)
            box_high, _ = yesterday_box(df)
            print(f"\n=== {datetime.utcnow().isoformat()} UTC ===")
            check_signal(df, box_high)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5 * 60)


if __name__ == "__main__":
    main()
