# BTC Sniper Bot

Small collection of scripts for testing trading ideas with Binance data.

## Available Scripts

- **btc_box_strategy.py** – one-off check of yesterday's range and basic indicators.
- **btc_box_loop.py** – polls every 5 minutes and prints a BUY signal when the price is above yesterday's high, above the 50‑period EMA, and RSI is over 60.

All scripts require `requests` and `pandas` installed. They expect internet access to reach the Binance API.
