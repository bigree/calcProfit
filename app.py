import streamlit as st
import requests

# メインアプリ
st.title("メルカリ利益計算ツール")

# 入力セクション
st.header("仕入れ価格と販売価格から利益を計算する")
supplier_price = st.number_input("仕入れ価格", min_value=0, step=1)
selling_price = st.number_input("販売価格", min_value=0, step=1)
shipping_cost = st.number_input("送料", min_value=0, step=1)
fee_percentage = st.slider("販売手数料率(%)", min_value=0, max_value=20, step=1, value=10)

if st.button("計算する"):
    # 計算ロジック
    selling_fee = selling_price * (fee_percentage / 100)
    net_income = selling_price - shipping_cost - selling_fee
    profit = net_income - supplier_price
    profit_rate = (profit / selling_price) * 100 if selling_price > 0 else 0

    st.subheader("計算結果")
    st.write(f"**仕入れ価格:** {supplier_price}円")
    st.write(f"**販売価格:** {selling_price}円")
    st.write(f"**送料:** {shipping_cost}円")
    st.write(f"**販売手数料:** {selling_fee:.2f}円")
    st.write(f"**手元に入る金額:** {net_income:.2f}円")
    st.write(f"**利益:** {profit:.2f}円")
    st.write(f"**利益率:** {profit_rate:.2f}%")

# ウォン→円換算セクション
st.header("ウォン→円換算")

# 為替レートを取得する関数
def get_exchange_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/KRW")
        data = response.json()
        return data["rates"]["JPY"]
    except Exception as e:
        st.error("為替レートの取得に失敗しました。デフォルト値を使用します。")
        return 0.1  # デフォルト値

exchange_rate = get_exchange_rate()
st.write(f"現在の為替レート: 1ウォン = {exchange_rate:.2f}円")

won_amount = st.number_input("金額(ウォン)", min_value=0, step=1)

if st.button("換算する"):
    yen_amount = won_amount * exchange_rate
    st.subheader("換算結果")
    st.write(f"**{won_amount}ウォンは {yen_amount:.2f}円です。**")
