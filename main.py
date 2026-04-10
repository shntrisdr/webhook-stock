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
                print(f"❌ {ticker}: データ不足（件数: {len(df) if not df.empty else 0}）")
                continue

            # 2. 【ここが最重要】二重構造（MultiIndex）の解除
            # 列名が ('Volume', '5803.T') のようになっている場合、最初の 'Volume' だけを抽出
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # 3. データの抽出を「位置(iloc)」ベースで行う
            # Series形式で残らないよう、values[index] で純粋な数値を取り出す
            volumes = df['Volume'].values
            
            # 念のため1次元配列に変換
            volumes = volumes.flatten()
            
            today_vol = float(volumes[-1])
            avg_vol = float(volumes[-21:-1].mean())

            print(f"📊 {ticker}: 本日出来高={today_vol:,.0f}, 20日平均={avg_vol:,.0f}")

            # 4. 判定
            if avg_vol > 0 and today_vol > avg_vol * 2.0:
                print(f"🚀 【判定】{ticker} は出来高急増（{today_vol/avg_vol:.1f}倍）です！")
            else:
                print(f"💤 {ticker} は平常運転です。")

        except Exception as e:
            print(f"⚠️ {ticker} 処理中にエラー発生: {e}")
            import traceback
            traceback.print_exc() # 詳細なエラー箇所を出力

if __name__ == "__main__":
    check_logic()
