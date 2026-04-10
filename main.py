import yfinance as yf
import requests
import os

# 監視銘柄（後でセクター全体に拡張可能）
TICKERS = ["5803.T", "5805.T", "5802.T"] # フジクラ, SWCC, 住友電工
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def check_logic():
    alerts = []
    for ticker in TICKERS:
        data = yf.download(ticker, period="1mo", interval="1d")
        if len(data) < 21: continue

        # 出来高スパイク判定（当日 > 20日平均 * 2.0）
        avg_vol = data['Volume'].iloc[-21:-1].mean()
        today_vol = data['Volume'].iloc[-1]
        
        if today_vol > avg_vol * 2.0:
            alerts.append(f"🚀 【出来高急増】{ticker}: 通常の{today_vol/avg_vol:.1f}倍")

    if alerts and DISCORD_WEBHOOK_URL:
        message = "\n".join(alerts)
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

if __name__ == "__main__":
    check_logic()
