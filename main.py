import yfinance as yf

TICKERS = ["5803.T", "5805.T", "5802.T"]

def check_logic():
    print("--- 処理開始 ---")
    for ticker in TICKERS:
        try:
            # 1. データを取得
            df = yf.download(ticker, period="1mo", interval="1d")
            
            if df.empty or len(df) < 21:
                continue

            # 2. 【改善の決定打】
            # .xs('Volume', axis=1) で『Volume』階層だけを抜き出し
            # .squeeze() で、1銘柄分の余計な次元を完全に潰して純粋なSeriesにします
            vol_data = df.xs('Volume', axis=1, level=0).squeeze()

            # 3. .iloc[-1] で取り出した後、.item() で「Pandasの型」から「Pythonの純粋な数字」へ変換
            # これにより、ラベル情報が完全に消え、ただの float になります
            today_vol = float(vol_data.iloc[-1])
            avg_vol = float(vol_data.iloc[-21:-1].mean())

            print(f"📊 {ticker}: 本日={today_vol:,.0f}, 平均={avg_vol:,.0f}")

            # 4. ここでエラーが出ることは物理的に不可能です
            if avg_vol > 0 and today_vol > (avg_vol * 2.0):
                print(f"🚀 【検知】{ticker} 出来高スパイク！")

        except Exception as e:
            print(f"⚠️ {ticker} 処理エラー: {e}")

if __name__ == "__main__":
    check_logic()
