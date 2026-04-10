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

            # 2. 【ここが解決の鍵】
            # .flatten() よりも強力に、Volume列を「純粋な数値のリスト」に変換します
            # 構造がどうあれ、valuesで中身を取り出し、flattenで平坦化し、listに変換
            vol_list = df['Volume'].values.flatten().tolist()
            
            # 3. Python標準のリスト操作で計算（ここなら絶対にAmbiguousエラーは出ません）
            today_vol = float(vol_list[-1])
            past_vols = vol_list[-21:-1]
            avg_vol = sum(past_vols) / len(past_vols)

            print(f"📊 {ticker}: 本日={today_vol:,.0f}, 平均={avg_vol:,.0f}")

            # 4. 数値同士の比較なので確実に通ります
            if avg_vol > 0 and today_vol > avg_vol * 2.0:
                print(f"🚀 {ticker}: 出来高スパイク検知！")

        except Exception as e:
            print(f"⚠️ {ticker} 処理エラー: {e}")

if __name__ == "__main__":
    check_logic()
