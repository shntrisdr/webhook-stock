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

            # 2. 【新アプローチ】Pandasのインデックスやカラムを無視して、
            # rawデータを「数値の2次元配列」として取得し、Volumeの列（通常は5番目）を特定する
            # indexではなく名前で安全に列番号を探す
            try:
                # どんな多重構造でも、列の1階層目に 'Volume' がある場所を特定
                vol_idx = [i for i, col in enumerate(df.columns) if 'Volume' in str(col)][0]
                # .values を使うことで Numpy配列になり、[行, 列] で純粋な数値が取れる
                all_volumes = df.values[:, vol_idx].flatten()
                
                # リスト化して「ただの数字」にする
                vol_list = [float(v) for v in all_volumes]
            except Exception:
                print(f"❌ {ticker}: Volume列の特定に失敗")
                continue

            # 3. ここからは Python 標準のリスト計算
            today_vol = vol_list[-1]
            avg_vol = sum(vol_list[-21:-1]) / 20

            print(f"📊 {ticker}: 本日={today_vol:,.0f}, 平均={avg_vol:,.0f}")

            # 4. ここでエラーが出るはずはありません（純粋な float 同士の比較）
            if avg_vol > 0 and today_vol > avg_vol * 2.0:
                print(f"🚀 【検知】{ticker} 出来高スパイク！")

        except Exception as e:
            print(f"⚠️ {ticker} 処理エラー: {e}")

if __name__ == "__main__":
    check_logic()
