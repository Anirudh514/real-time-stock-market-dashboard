import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


st.set_page_config(
    page_title="Real-Time Stock Market Dashboard",
    page_icon="📈",
    layout="wide" 
)


st.title("Real Time Stoc Market Dashboard")

st.write(
    "Track and viisualize stock market data using"
    "Python,Pandas,Plotly,and Streamlit."
)


st.sidebar.header("Dashboard Settings")

popular_stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Meta": "META",
    "Netflix": "NFLX",

    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "SBI": "SBIN.NS"
}


selected_stock = st.sidebar.selectbox(
    "Select a stock",
    list(popular_stocks.keys())
)


ticker = popular_stocks[selected_stock]


custom_ticker = st.sidebar.text_input(
    "Or enter a ticker symbol",
    placeholder="Example: AAPL"
)


if custom_ticker.strip():
    ticker = custom_ticker.strip().upper()



period = st.sidebar.selectbox(
    "Select time period",
    [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y"
    ],
    index=5
)



@st.cache_data(ttl=300)
def download_data(symbol, selected_period):

    data = yf.download(
        symbol,
        period=selected_period,
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    return data


try:

    data = download_data(
        ticker,
        period
    )

except Exception as error:

    st.error(
        f"Error while downloading data: {error}"
    )

    st.stop()



if data.empty:

    st.error(
        "No stock data found. Please check the ticker symbol."
    )

    st.stop()


# Handle MultiIndex columns
if isinstance(data.columns, pd.MultiIndex):

    data.columns = data.columns.get_level_values(0)




data["MA20"] = data["Close"].rolling(20).mean()

data["MA50"] = data["Close"].rolling(50).mean()


latest_price = float(data["Close"].iloc[-1])


if len(data) >= 2:

    previous_price = float(data["Close"].iloc[-2])

else:

    previous_price = latest_price


price_change = latest_price - previous_price


percentage_change = (
    price_change / previous_price
) * 100


highest_price = float(data["High"].max())

lowest_price = float(data["Low"].min())




st.subheader(
    f"📊 {ticker} Market Overview"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Latest Price",
        f"{latest_price:,.2f}",
        f"{price_change:,.2f}"
    )


with col2:

    st.metric(
        "Change %",
        f"{percentage_change:.2f}%"
    )


with col3:

    st.metric(
        "Highest Price",
        f"{highest_price:,.2f}"
    )


with col4:

    st.metric(
        "Lowest Price",
        f"{lowest_price:,.2f}"
    )




st.subheader("📈 Stock Price Chart")


fig = go.Figure()


fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Closing Price"
    )
)


fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["MA20"],
        mode="lines",
        name="20-Day Moving Average"
    )
)


fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["MA50"],
        mode="lines",
        name="50-Day Moving Average"
    )
)


fig.update_layout(
    title=f"{ticker} Price Movement",
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified",
    height=550
)


st.plotly_chart(
    fig,
    use_container_width=True
)




st.subheader("📊 Trading Volume")


volume_fig = go.Figure()


volume_fig.add_trace(
    go.Bar(
        x=data.index,
        y=data["Volume"],
        name="Trading Volume"
    )
)


volume_fig.update_layout(
    title="Trading Volume",
    xaxis_title="Date",
    yaxis_title="Volume",
    height=400
)


st.plotly_chart(
    volume_fig,
    use_container_width=True
)



st.subheader("📋 Historical Stock Data")


show_data = st.checkbox(
    "Show historical data"
)


if show_data:

    st.dataframe(
        data,
        use_container_width=True
    )




csv_data = data.to_csv().encode("utf-8")


st.download_button(
    label="⬇️ Download CSV",
    data=csv_data,
    file_name=f"{ticker}_stock_data.csv",
    mime="text/csv"
)




st.markdown("---")


st.caption(
    "Built with Python, Pandas, yfinance, Plotly and Streamlit."
)


st.caption(
    f"Application refresh: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

    


st.warning(
    "This project is for educational purposes only "
    "and is not financial advice."
)


