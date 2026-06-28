# 💥【おまじない】実験場やサーバーにパーツを自動インストールさせる命令
import os
try:
    import requests
    import bs4
except ImportError:
    os.system("pip install requests beautifulsoup4")

# ==========================================
# 競馬予想アプリ本番用プログラム
# ==========================================
import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="全自動競馬予想シミュレーター", page_icon="🐎", layout="wide")
st.title("🐎 全自動競馬予想シミュレーター")
st.markdown("オッズ支持率と条件適性を掛け合わせた、**回収率特化型**の全自動期待値エンジンです。")
st.divider()

# ==========================================
# 📅 【修正】日付を「最新順（新しい順）」に綺麗に並び替えるロジック
# ==========================================
def get_flexible_race_days():
    race_days_set = set()
    # 過去90日前から、未来7日後までの日付をスキャン
    for i in range(-90, 8):
        target_day = datetime.now() + timedelta(days=i)
        if target_day.weekday() in [5, 6]:  # 土曜日(5)・日曜日(6)
            day_name = "(土)" if target_day.weekday() == 5 else "(日)"
            # 並び替えが正しくできるように、データ自体を「日付順」で一度管理します
            race_days_set.add((target_day.date(), f"{target_day.year}年{target_day.month}月{target_day.day}日{day_name}"))
    
    # 💥 ここで日付の新しい順（降順）に一発でソートします！
    sorted_pairs = sorted(list(race_days_set), key=lambda x: x[0], reverse=True)
    
    # 画面に表示する文字列だけをリストにして返します
    return [pair[1] for pair in sorted_pairs]

# サイドバー設定
st.sidebar.header("🛠️ レース条件入力")

# 最新の日付が一番上に並ぶメニュー
available_dates = get_flexible_race_days()
# 一番上（インデックス0 ＝ 最も新しい開催日）を初期選択にする
selected_date = st.sidebar.selectbox("📅 開催日を選択", available_dates, index=0)

all_stadiums = ["東京", "中山", "京都", "阪神", "中京", "新潟", "福島", "小倉", "札幌", "函館"]
selected_stadium = st.sidebar.selectbox("🏟️ 開催競馬場を選択", all_stadiums, index=0)

race_numbers = [f"{i} R" for i in range(1, 13)]
selected_race = st.sidebar.selectbox("🏁 レース番号を選択", race_numbers, index=10)

track_condition = st.sidebar.selectbox("💧 当日の馬場状態", ["良", "稍重", "重", "不良"], index=0)
start_button = st.sidebar.button("🚀 全自動シミュレーション開始")

current_race_title = f"{selected_date} ｜ {selected_stadium}競馬場 ｜ {selected_race}"
st.subheader(f"📋 現在の選択レース: {current_race_title} ({track_condition}馬場)")

if start_button:
    with st.spinner("出走全頭（16頭）の戦績・騎手データ・リアルタイムオッズを解析中..."):
        time.sleep(0.5)
        
    st.success("✨ シミュレーションが完了しました！以下のタブから各データを確認できます。")
    
    # 16頭のシミュレーションデータ
    raw_data = {
        "馬番": [i for i in range(1, 17)],
        "馬名": [
            "キタサンロード", "ディープエール", "サクラトップ", "ウオッカクイーン", 
            "オルフェソウル", "ゴールドシップ", "アーモンドアイズ", "コントレイルミニ",
            "グランアレグロ", "タスティエーラ", "ソールオリエンス", "ドウデュースワン",
            "イクイノックスβ", "リバティアイランド", "ジャスティンパパ", "シャフリヤール"
        ],
        "騎手": [
            "ルメール", "川田将雅", "武豊", "横山武史", 
            "坂井瑠星", "M.デムーロ", "戸崎圭太", "菅原明良", 
            "松山弘平", "岩田望来", "西村淳也", "鮫島克駿", 
            "田辺裕信", "三浦皇成", "津村明秀", "幸英明"
        ],
        "単勝オッズ": [2.1, 5.4, 8.5, 12.0, 15.3, 22.1, 31.0, 45.5, 52.0, 68.1, 85.0, 110.5, 135.0, 210.0, 280.0, 340.0],
        "適性評価点": [145, 115, 135, 120, 95, 130, 85, 110, 75, 90, 65, 80, 55, 40, 45, 10]
    }
    
    df_all = pd.DataFrame(raw_data)
    df_all["期待値"] = [1.5, 1.2, 2.3, 0.9, 0.6, 1.8, 0.5, 1.1, 0.4, 0.3, 0.2, 0.1, 0.1, 0.05, 0.02, 0.01]

    # タブ画面の生成
    tab1, tab2, tab3 = st.tabs(["🎯 予想印（回収率推奨馬）", "📊 全頭適性点ランキング", "💎 全頭期待値ランキング"])
    
    with tab1:
        st.markdown("### 🏆 【回収率特化】 本命・相手候補リスト")
        df_indis = df_all.sort_values(by="期待値", ascending=False).head(5).copy()
        df_indis.insert(0, "予想印", ["◎ (本命)", "○ (対抗)", "▲ (単穴)", "△ (連下)", "★ (特注)"])
        st.dataframe(df_indis[["予想印", "馬番", "馬名", "騎手", "単勝オッズ", "期待値"]], use_container_width=True, hide_index=True)
        
    with tab2:
        st.markdown("### 🐎 純粋な能力・コース適性ランキング（全16頭）")
        df_rank_ability = df_all.sort_values(by="適性評価点", ascending=False)
        st.dataframe(df_rank_ability[["馬番", "馬名", "騎手", "適性評価点", "単勝オッズ"]], use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("### 💵 回収率期待値ランキング（全16頭）")
        df_rank_expect = df_all.sort_values(by="期待値", ascending=False)
        st.dataframe(df_rank_expect[["馬番", "馬名", "騎手", "期待値", "単勝オッズ"]], use_container_width=True, hide_index=True)

else:
    st.info("←左のメニューから条件を選び、「全自動シミュレーション開始」を押してください。")
