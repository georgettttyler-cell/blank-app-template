import streamlit as st
import pandas as pd
import requests

# 1. Setup
st.set_page_config(page_title="Equity-Sentiment Bridge", layout="wide")
st.title("📊 Equity-Sentiment Bridge")
st.write(" Bridge between Valuation & Marketing")

# 2. Sidebar for Inputs
st.sidebar.header("Control Panel")
ticker = st.sidebar.text_input("Enter US Stock Ticker (e.g., TSLA, AAPL, MSFT):", "AAPL").upper()
# REPLACE 'YOUR_API_KEY' with the key you got from Alpha Vantage
API_KEY = '7KGG22B5ZBR5C1JM' 

# 3. Fetch Real Price (The "Finance" part)
def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    return float(data['Global Quote']['05. price'])

try:
    current_price = get_stock_price(ticker)
    
    # 4. Sentiment Slider (The "Marketing" part)
    sentiment = st.slider("Current Brand Sentiment Score (Social Media/News)", 0, 100, 50)
    
    # Logic: Sentiment > 70 adds a 15% premium. Sentiment < 30 adds a 20% discount.
    multiplier = 1.0
    if sentiment > 70: multiplier = 1.15
    elif sentiment < 30: multiplier = 0.80
    
    adjusted_price = current_price * multiplier

    # 5. Display Results
    col1, col2 = st.columns(2)
    col1.metric("Current Market Price", f"${current_price:.2f}")
    col2.metric("Brand-Adjusted 'Fair Value'", f"${adjusted_price:.2f}", f"{((multiplier-1)*100):.1f}%")

    st.bar_chart(pd.DataFrame({
        "Valuation Type": ["Standard Market Price", "Marketing-Adjusted Value"],
        "Price ($)": [current_price, adjusted_price]
    }).set_index("Valuation Type"))

except:
    st.error("Please enter a valid Ticker or check your API Key limit.")
