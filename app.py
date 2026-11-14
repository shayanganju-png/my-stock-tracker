import streamlit as st
import yfinance as yf
if "portfolio_list" not in st.session_state:
    st.session_state.portfolio_list=[]
st.title("📈 My Personal Stock Watchlist")

# Inputs to add a stock to your watchlist
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, NVDA):").upper()
target_price = st.number_input("Enter your target 'BUY' price ($):", min_value=0.0, value=100.0)
notes = st.text_area("Why are you watching this stock?")

# Save and display the target alert
if st.button("Add to Watchlist"):
    if ticker != "":
        st.success(f"Added {ticker} to your tracking dashboard!")
        stock_package = {
            "symbol": ticker,
            "qty": 10,
            "avg_price": target_price
        }
        st.session_state.portfolio_list.append(stock_package)       
    else:
        st.error("Please enter a valid stock ticker symbol.")
        st.write("---")
st.subheader("📋 Portfolio Summary View")
for item in st.session_state.portfolio_list:
 # Calculate the profit or loss percent
    pct_change = ((item['live_price'] - item['buy_price']) / item['buy_price']) * 100

    if pct_change >= 0:
        st.success(f"🔺 {item['symbol']} | Live: ${item['live_price']:.2f} | Gain: +{pct_change:.2f}%")
    else:
        st.error(f"🔻 {item['symbol']} | Live: ${item['live_price']:.2f} | Loss: {pct_change:.2f}%")
