import yfinance as yf
import requests
import os

# 監視銘柄
TICKERS = ["5803.T", "5805.T", "5802.T"]
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def check_logic():
    alerts = []
    for ticker in TICKERS:
        # dataを取得。auto_adjust=Trueで構造を安定させます
        df = yf.download(ticker, period="1mo", interval="1d", auto_adjust=True)
        
        if len(df) < 21:
            continue

        # 【修正ポイント】 .iloc を使って「位置」で指定し、さらに確実に1つの数値（scalar）に変換します
        # df['Volume'] が2次元（DataFrame）になっていても、ilocなら正しく抽出できます
        try:
            # 最新日の出来高
            today_vol = float(df['Volume'].iloc[-1])
            # 過去20日（当日除く）の平均出来高
            avg_vol = float(df['Volume'].iloc[-21:-1].mean())
            
            if avg_vol > 0 and today_vol > avg_vol * 2.0:
                alerts.append(f"🚀 【出来高急増】{ticker}: 通常の{today_vol/avg_vol:.1f}倍")
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    if alerts and DISCORD_WEBHOOK_URL:
        message = "\n".join(alerts)
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    else:
        print("No alerts or Webhook URL missing.")

if __name__ == "__main__":
    check_logic()
