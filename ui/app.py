
import streamlit as st

st.set_page_config(
    page_title="FinSentIQ",
    page_icon="📈",
    layout="wide"
)

st.title("FinSentIQ — Financial Sentiment Intelligence")
st.markdown("---")

st.markdown("""
### Welcome to FinSentIQ!
Use the sidebar to navigate between pages:

- **Live News Analyzer**   — Analyze live financial headlines
- **Stock Sentiment**      — Get sentiment for any stock
- **Fear & Greed Meter**   — See current market mood score
- **Market Mood Tracker**  — Track mood changes over time
""")

st.markdown("---")
st.info("Select a page from the sidebar to get started!")
