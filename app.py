import streamlit as st
import yfinance as yf
import plotly.express as px
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
        
        #  Download live market data from Wall Street
          stock_data_fetch = yf.download(ticker, period="5d", multi_level_index=False)
          live_market_price = float(stock_data_fetch['Close'].iloc[-1])
         #  Download a longer 50-day timeline to check market trends
          history_data = yf.download(ticker, period="50d", multi_level_index=False)
        
        #  Calculate the short-term trend vs long-term trend
          short_trend = float(history_data['Close'].rolling(window=10).mean().iloc[-1])
          long_trend = float(history_data['Close'].rolling(window=30).mean().iloc[-1])
        
        # Core Decision Logic: Compare the trends to create a Buy/Sell signal
          if short_trend > long_trend:
            signal = "🟢 STRONG BUY"
          else:
            signal = "🔴 SELL / AVOID"
        # Package everything up with the dictionary labels
          stock_package = {
            "symbol": ticker,
            "qty": 10,
            "buy_price": target_price,
            "live_price": live_market_price,
            "status_signal": signal  
        }
          
          st.session_state.portfolio_list.append(stock_package)       
    else:
        st.error("Please enter a valid stock ticker symbol.")
        st.write("---")
    st.subheader("📋 Portfolio Summary View")
for item in st.session_state.portfolio_list:
    pct_change = ((item['live_price'] - item['buy_price']) / item['buy_price']) * 100

    if pct_change >= 0:
        st.success(f"🔺 {item['symbol']} | Live: ${item['live_price']:.2f} | Gain: +{pct_change:.2f}% | Advice: {item['status_signal']}")
    else:
        st.error(f"🔻 {item['symbol']} | Live: ${item['live_price']:.2f} | Loss: {pct_change:.2f}% | Advice: {item['status_signal']}")

if len(st.session_state.portfolio_list) > 0:    
    last_stock = st.session_state.portfolio_list[-1]['symbol']
    chart_data = yf.download(last_stock, period="50d", multi_level_index=False)
# Use mathematical mapping to see if each day closed higher (+) or lower (-) than the day before
    chart_data['Price_Change'] = chart_data['Close'].diff()
    
# Assign color flags based on daily performance logic
    chart_data['Color_Flag'] = ['#00cc66' if x >= 0 else '#ff3333' for x in chart_data['Price_Change']]
    
# Build a visual dynamic Bar Chart instead of a solid line
    fig = px.bar(
        chart_data,
        y="Close",
        title=f"Market Block Trajectory: {last_stock}",
        color="Color_Flag",
        color_discrete_map="identity"
    )
    
# Hide the background side legends so the dashboard looks perfectly clean
    fig.update_layout(showlegend=False)
