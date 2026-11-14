import streamlit as st

st.title("📈 My Personal Stock Watchlist")

# 1. Inputs to add a stock to your watchlist
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, NVDA):").upper()
target_price = st.number_input("Enter your target 'BUY' price ($):", min_value=0.0, value=100.0)
notes = st.text_area("Why are you watching this stock?")

# 2. Save and display the target alert
if st.button("Add to Watchlist"):
    if ticker != "":
        st.success(f"Added {ticker} to your tracking dashboard!")
        
        # Display a clean data card for your app portfolio
        st.metric(label=f"{ticker} Target Price", value=f"${target_price:.2f}")
        st.info(f"📋 Investment Thesis: {notes}")
    else:
        st.error("Please enter a valid stock ticker symbol.")
