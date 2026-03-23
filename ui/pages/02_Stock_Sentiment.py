
import streamlit as st
import sys
sys.path.append("/content/finsentiq/services")
from all_services import fetch_all_news, analyze_sentiment, fetch_stock_data

st.title("Stock Sentiment Analyzer")
st.markdown("Get full sentiment analysis for any stock")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    ticker = st.text_input("Enter Stock Ticker:", placeholder="e.g. TSLA, AAPL, RELIANCE.NS")
with col2:
    company = st.text_input("Enter Company Name:", placeholder="e.g. Tesla, Apple, Reliance")

if st.button("Get Stock Sentiment"):
    if ticker and company:
        with st.spinner(f"Analyzing {ticker}..."):

            # Fetch stock data
            stock = fetch_stock_data(ticker)

            # Fetch & analyze news
            headlines  = fetch_all_news(f"{company} stock", max_results=5)
            sentiments = [analyze_sentiment(h) for h in headlines]
            positive   = sum(1 for s in sentiments if s["sentiment"] == "POSITIVE")
            negative   = sum(1 for s in sentiments if s["sentiment"] == "NEGATIVE")
            overall    = "POSITIVE" if positive > negative else "NEGATIVE" if negative > positive else "NEUTRAL"

            # Display stock info
            st.markdown("---")
            st.subheader(f"{ticker} Live Data")
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price",  f"${stock['price']}")
            col2.metric("Daily Change",   f"{stock['change']}%")
            col3.metric("5 Day Trend",    stock["trend"])

            st.markdown("---")
            st.subheader("News Sentiment")
            col1, col2, col3 = st.columns(3)
            col1.metric("Overall Sentiment", overall)
            col2.metric("Positive News",     positive)
            col3.metric("Negative News",     negative)

            # Show headlines
            st.markdown("---")
            st.subheader("Headlines Analyzed")
            for i, (headline, sentiment) in enumerate(zip(headlines, sentiments), 1):
                color = "green" if sentiment["sentiment"] == "POSITIVE" else "red" if sentiment["sentiment"] == "NEGATIVE" else "gray"
                st.markdown(f"{i}. {headline}")
                st.markdown(f"   -> :{color}[{sentiment['sentiment']}] ({sentiment['confidence']}%)")
    else:
        st.warning("Please enter both ticker and company name!")
