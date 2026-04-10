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

            # 2. 【ここが最重要】Pandasを捨てて「純粋な数値リスト」に変換
            # to_dict('list')を使うことで、どんな階層構造であっても
            # {'Volume': [100, 200, ...]} という単純な辞書になります
            data_dict = df.to_dict('list')
            
            # 辞書のキー名が ('Volume', '5803.T') のようになっている場合があるため、
            # キーの中に 'Volume' が含まれているものを探して数値リストを抽出します
            vol_list = []
            for key, values in data_dict.items():
                if isinstance(key, tuple):
                    if 'Volume' in key:
                        vol_list = values
                        break
                elif key == 'Volume':
                    vol_list = values
                    break

            if not vol_list:
                print(f"❌ {ticker}: Volumeデータが見つかりません。")
                continue

            # 3. Python標準の数値として計算
            today_vol = float(vol_list[-1])
            past_20_vols = vol_list[-21:-1]
            avg_vol = sum(past_20_vols) / len(past_20_vols)

            print(f"📊 {ticker}: 本日={today_vol:,.0f}, 平均={avg_vol:,.0f}")

            # 4. 純粋なfloat同士の比較なので、絶対にエラーは出ません
            if avg_vol > 0 and today_vol > avg_vol * 2.0:
                print(f"🚀 【検知】{ticker}: 出来高スパイク（{today_vol/avg_vol:.1f}倍）")

        except Exception as e:
            print(f"⚠️ {ticker} 処理エラー: {e}")

if __name__ == "__main__":
    check_logic()
