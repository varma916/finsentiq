
import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../services"))
from all_services import fetch_all_news, calculate_fear_greed

st.title("Fear & Greed Meter")
st.markdown("Real-time market fear and greed index powered by NLP")
st.markdown("---")

topic = st.selectbox(
    "Select Market Topic:",
    ["stock market today", "S&P 500", "Nasdaq", "cryptocurrency", "global economy"]
)

if st.button("Calculate Fear & Greed Score"):
    with st.spinner("Analyzing market sentiment..."):
        headlines = fetch_all_news(topic, max_results=8)
        result    = calculate_fear_greed(headlines)
        score     = result["score"]
        meter     = result["meter"]

        if score <= 20:   color = "red"
        elif score <= 40: color = "orange"
        elif score <= 60: color = "gray"
        elif score <= 80: color = "lightgreen"
        else:             color = "green"

        fig = go.Figure(go.Indicator(
            mode  = "gauge+number",
            value = score,
            title = {"text": f"Fear & Greed Index — {meter}"},
            gauge = {
                "axis": {"range": [0, 100]},
                "bar":  {"color": color},
                "steps": [
                    {"range": [0,  20], "color": "red"},
                    {"range": [20, 40], "color": "orange"},
                    {"range": [40, 60], "color": "lightgray"},
                    {"range": [60, 80], "color": "lightgreen"},
                    {"range": [80, 100],"color": "green"},
                ],
                "threshold": {
                    "line":  {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": score
                }
            }
        ))

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Score",              f"{score}/100")
        col2.metric("Meter",              meter)
        col3.metric("Headlines Analyzed", len(headlines))

        st.markdown("---")
        st.subheader("Headlines Used")
        for i, headline in enumerate(headlines, 1):
            st.markdown(f"{i}. {headline}")
