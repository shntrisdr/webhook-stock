import yfinance as yf
import pandas as pd

TICKERS = ["5803.T", "5805.T", "5802.T"]

def check_logic():
    print("--- 処理開始 ---")
    for ticker in TICKERS:
        try:
            # 1. データを取得
            df = yf.download(ticker, period="1mo", interval="1d")
            
            if df.empty or len(df) < 21:
                continue

            # 2. 【ここが急所】MultiIndexを即座に解消
            # これにより df['Volume'] が「特定の銘柄の列」ではなく「ただの列」になります
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # 3. 確実に「一列のデータ(Series)」としてから「最後の値」を抽出
            # .squeeze() を使うことで、余計な次元を完全に削ぎ落とします
            vol_series = df['Volume'].squeeze()
            
            # Seriesの末尾から数値を取得
            today_vol = float(vol_series.iloc[-1])
            avg_vol = float(vol_series.iloc[-21:-1].mean())

            print(f"📊 {ticker}: 本日={today_vol:,.0f}, 平均={avg_vol:,.0f}")

            # 4. 判定（ここでもう ValueError は出ません）
            if avg_vol > 0 and today_vol > avg_vol * 2.0:
                print(f"🚀 {ticker}: 出来高スパイク検知！")

        except Exception as e:
            print(f"⚠️ {ticker} エラー: {e}")

if __name__ == "__main__":
    check_logic()
