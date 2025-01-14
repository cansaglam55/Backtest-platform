
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Uygulama Başlığı
st.title("US100 Analiz Aracı - Tam Donanımlı")

# Kullanıcıdan parametreler alınıyor
symbol = "^NDX"  # US100 için sembol
interval = st.selectbox(
    "Zaman Dilimini Seçin",
    options=["1m", "3m", "5m", "15m", "30m", "45m", "1h", "4h", "1d", "1wk", "1mo"],
    index=7,  # Varsayılan olarak 1 günlük
)
start_date = (datetime.today() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")
end_date = datetime.today().strftime("%Y-%m-%d")

# Renk özelleştirme
color_up = st.color_picker("Yükseliş Rengi (Yeşil)", "#00FF00")
color_down = st.color_picker("Düşüş Rengi (Kırmızı)", "#FF0000")

# Veriyi çekme ve grafiği oluşturma
if st.button("Grafiği Çiz"):
    try:
        st.write(f"{symbol} verisi çekiliyor ({start_date} - {end_date})...")
        data = yf.download(tickers=symbol, start=start_date, end=end_date, interval=interval)

        if not data.empty:
            # Mum grafiği
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                increasing_line_color=color_up,
                decreasing_line_color=color_down
            )])
            fig.update_layout(
                title=f"{symbol} - {interval} Zaman Dilimi",
                xaxis_title="Tarih",
                yaxis_title="Fiyat",
                template="plotly_dark",
            )
            st.plotly_chart(fig)
        else:
            st.error("Seçilen zaman dilimi için veri bulunamadı.")
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")

st.write("US100 verisini detaylı incelemek için bu aracı kullanabilirsiniz!")
