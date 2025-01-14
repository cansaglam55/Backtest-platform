
import streamlit as st
import yfinance as yf
import pandas as pd

# Arayüz Başlığı
st.title("US100 Backtest Platformu")

# Kullanıcıdan girdi alma
symbol = st.text_input("Parite İsmi", value="^NDX")
start_date = st.date_input("Başlangıç Tarihi", value=pd.to_datetime("2023-01-01"))
end_date = st.date_input("Bitiş Tarihi", value=pd.to_datetime("2024-01-01"))
short_window = st.number_input("Kısa Dönem MA", min_value=1, max_value=50, value=10)
long_window = st.number_input("Uzun Dönem MA", min_value=20, max_value=200, value=50)

# Veri çekme
if st.button("Veriyi Çek ve Backtest Yap"):
    data = yf.download(symbol, start=start_date, end=end_date)
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()

    # Strateji sinyalleri
    data['Signal'] = 0
    data['Signal'][short_window:] = (data['Short_MA'][short_window:] > data['Long_MA'][short_window:]).astype(int)
    data['Position'] = data['Signal'].diff()

    # Performans hesaplama
    initial_balance = 10000
    data['Daily_Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Daily_Return'] * data['Signal'].shift(1)
    data['Portfolio_Value'] = initial_balance * (1 + data['Strategy_Return']).cumprod()

    # Grafik
    st.line_chart(data[['Portfolio_Value']])
    st.write("Backtest sonuçları:", data)
