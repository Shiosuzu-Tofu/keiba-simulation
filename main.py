import streamlit as st
import pandas as pd

# ページ設定
st.set_page_config(page_title="スプレッドシート連動型競馬予想", layout="wide")
st.title("🐎 競馬予想シミュレーション")
st.markdown("Googleスプレッドシートのデータを読み込み、自動で期待値を算出します。")

# ==========================================
# ⚙️ 設定：あなたのスプレッドシートIDを入力
# ==========================================
# ※スプレッドシートのURLが https://docs.google.com/spreadsheets/d/abc123456789/edit... 
# の場合、「abc123456789」の部分がIDです。
SHEET_ID = "https://docs.google.com/spreadsheets/d/1gVBeCGgOSV2GvSn-ZfH8VN41kr7jcsRzdtW7cyB7iYE/edit?gid=0#gid=0"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

def load_data():
    try:
        # スプレッドシートを読み込む
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"データの読み込みに失敗しました。URLや共有設定を確認してください: {e}")
        return None

# サイドバーに操作ボタン
st.sidebar.header("📊 データ更新")
if st.sidebar.button("🔄 最新データを取得"):
    df = load_data()
    
    if df is not None:
        st.success("スプレッドシートからデータを取得しました！")
        
        # データの表示
        st.subheader("📋 元データ")
        st.dataframe(df, use_container_width=True)
        
        # 期待値の計算（適性評価点 ÷ 単勝オッズ）
        if "適性評価点" in df.columns and "単勝オッズ" in df.columns:
            df["期待値"] = df["適性評価点"] / df["単勝オッズ"]
            
            st.subheader("💎 期待値ランキング")
            # 期待値が高い順に表示
            df_result = df.sort_values(by="期待値", ascending=False)
            st.dataframe(df_result.style.format({"期待値": "{:.2f}"}), use_container_width=True)
        else:
            st.warning("シートに「適性評価点」と「単勝オッズ」という項目があるか確認してください。")
else:
    st.info("←左のボタンを押すと、スプレッドシートのデータが読み込まれます。")
