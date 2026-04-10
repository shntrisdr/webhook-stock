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

            # 2. 【ここが最重要】
            # df['Volume'] を使うと「どの銘柄の？」という情報が付いてくるので、
            # columnsの内容を無視して、全データから「Volume」という文字を含む列を探し、
            # そのデータだけを「純粋な数値のリスト」として抽出します。
            vol_column = [col for col in df.columns if 'Volume' in str(col)]
            if not vol_column:
                continue
                
            # .tolist() を使って、Pandasオブジェクトから「Pythonの普通のリスト」へ変換
            # 二次元リストになる場合があるので .flatten() 的に処理
            raw_volumes = df[vol_column[0]].values.tolist()
            
            # リストがネストしている（[[1, 2, 3]]）場合の対策
            if isinstance(raw_volumes[0], list):
                vol_list = [float(v[0]) for v in raw_volumes]
            else:
                vol_list = [float(v) for v in raw_volumes]

            # 3. ここからは「ただの数字」の計算
            today_vol = vol_list[-1]
            past_20_vols = vol_list[-21:-1]
            avg_vol = sum(past_20_vols) / len(past_20_vols)

            print(f"📊 {ticker}: 本日={today_vol:,.0f}, 平均={avg_vol:,.0f}")

            # 4. 数値(float)同士の比較なので、絶対に ValueError は出ません
            if avg_vol > 0 and today_vol > (avg_vol * 2.0):
                print(f"🚀 【検知】{ticker} 出来高スパイク！")

        except Exception as e:
            print(f"⚠️ {ticker} 処理エラー: {e}")

if __name__ == "__main__":
    check_logic()
