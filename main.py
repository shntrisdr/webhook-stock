import yfinance as yf
import requests
import os

# 監視銘柄
TICKERS = ["5803.T", "5805.T", "5802.T"]
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def check_logic():
    alerts = []
    for ticker in TICKERS:
        # 1. データを取得
        df = yf.download(ticker, period="1mo", interval="1d")
        
        if df.empty or len(df) < 21:
            continue

        try:
            # 2. 【最重要】Volume列だけを抜き出し、さらに「銘柄名の階層」があればそれも剥がして1次元にする
            # どんな形であれ .values.flatten() で単純な数字のリストに変換します
            vols = df['Volume'].values.flatten()
            
            # 3. 1次元になったリストから数値を取り出す
            today_vol = float(vols[-1])
            avg_vol = float(vols[-21:-1].mean())
            
            # 4. 判定
            if avg_vol > 0 and today_vol > avg_vol * 2.0:
                alerts.append(f"🚀 【出来高急増】{ticker}: 通常の{today_vol/avg_vol:.1f}倍")
                
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    # 5. 通知
    if alerts and DISCORD_WEBHOOK_URL:
        message = "\n".join(alerts)
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        print("Alert sent!")
    else:
        print("No alerts or Webhook URL missing.")

if __name__ == "__main__":
    check_logic()
