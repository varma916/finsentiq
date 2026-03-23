
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
import sys
from datetime import datetime
sys.path.append("/content/finsentiq/services")
from all_services import fetch_all_news, calculate_fear_greed

st.title("Market Mood Tracker")
st.markdown("Track how market sentiment changes over multiple searches")
st.markdown("---")

# Initialize mood history in session state
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

topic = st.text_input("Enter topic to track:", placeholder="e.g. stock market, Tesla, Bitcoin")

if st.button("Track Mood Now"):
    if topic:
        with st.spinner("Analyzing current mood..."):
            headlines = fetch_all_news(topic, max_results=5)
            result    = calculate_fear_greed(headlines)
            score     = result["score"]
            meter     = result["meter"]
            timestamp = datetime.now().strftime("%H:%M:%S")

            st.session_state.mood_history.append({
                "time":  timestamp,
                "topic": topic,
                "score": score,
                "meter": meter
            })

            st.success(f"Mood tracked! Score -> {score}/100 ({meter})")
    else:
        st.warning("Please enter a topic!")

# Show mood chart if history exists
if st.session_state.mood_history:
    st.markdown("---")
    st.subheader("Mood History Chart")

    df = pd.DataFrame(st.session_state.mood_history)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x    = df["time"],
        y    = df["score"],
        mode = "lines+markers",
        name = "Fear & Greed Score",
        line = {"color": "blue", "width": 2},
        marker = {"size": 10}
    ))

    fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Neutral (50)")
    fig.add_hline(y=25, line_dash="dash", line_color="red",  annotation_text="Fear Zone (25)")
    fig.add_hline(y=75, line_dash="dash", line_color="green",annotation_text="Greed Zone (75)")

    fig.update_layout(
        xaxis_title = "Time",
        yaxis_title = "Fear & Greed Score",
        yaxis       = {"range": [0, 100]},
        height      = 400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Mood History Table")
    st.dataframe(df, use_container_width=True)

    if st.button("Clear History"):
        st.session_state.mood_history = []
        st.success("History cleared!")
else:
    st.info("Track a topic above to start building your mood history chart!")
