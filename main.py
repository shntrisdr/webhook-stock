import yfinance as yf
import pandas as pd

TICKERS = ["5803.T", "5805.T", "5802.T"]

def check_logic():
    print("--- 処理開始 ---")
    for ticker in TICKERS:
        try:
            # セッション指定なし。最新のyfinanceに任せる
            df = yf.download(ticker, period="1mo", interval="1d")
            
            if df.empty:
                print(f"❌ {ticker}: データが取得できませんでした。")
                continue

            # 二重構造（MultiIndex）を解除して平坦化
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # 数値として確実に取り出す（最新日のVolumeと、過去20日の平均）
            # .values.flatten() を使って次元の壁を壊す
            volumes = df['Volume'].values.flatten()
            today_vol = float(volumes[-1])
            avg_vol = float(volumes[-21:-1].mean())

            print(f"📊 {ticker}: 本日出来高={today_vol:,.0f}, 20日平均={avg_vol:,.0f}")

            if avg_vol > 0 and today_vol > avg_vol * 2.0:
                print(f"🚀 【判定】{ticker} は出来高急増（{today_vol/avg_vol:.1f}倍）です！")
            else:
                print(f"💤 {ticker} は平常運転です。")

        except Exception as e:
            print(f"⚠️ {ticker} 処理中にエラー: {e}")

if __name__ == "__main__":
    check_logic()
