
import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../services"))
from all_services import fetch_all_news, analyze_sentiment, detect_emotion

st.title("Live News Analyzer")
st.markdown("Analyze sentiment of live financial news headlines")
st.markdown("---")

query = st.text_input("Enter a topic or company:", placeholder="e.g. Tesla, Apple, Stock Market")

if st.button("Analyze News"):
    if query:
        with st.spinner("Fetching live news and analyzing..."):
            headlines = fetch_all_news(query, max_results=5)

            if not headlines:
                st.error("No headlines found. Try a different query.")
            else:
                st.success(f"{len(headlines)} headlines analyzed!")
                st.markdown("---")

                positive_count = 0
                negative_count = 0
                neutral_count  = 0

                for i, headline in enumerate(headlines, 1):
                    sentiment = analyze_sentiment(headline)
                    emotion   = detect_emotion(headline)

                    if sentiment["sentiment"] == "POSITIVE":
                        positive_count += 1
                        color = "green"
                    elif sentiment["sentiment"] == "NEGATIVE":
                        negative_count += 1
                        color = "red"
                    else:
                        neutral_count += 1
                        color = "gray"

                    with st.expander(f"Headline {i}: {headline[:80]}..."):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Sentiment:** :{color}[{sentiment['sentiment']}]")
                            st.markdown(f"**Confidence:** {sentiment['confidence']}%")
                            st.markdown(f"**Signal:** {sentiment['signal']}")
                        with col2:
                            st.markdown(f"**Primary Emotion:** {emotion['primary']}")
                            st.markdown(f"**Market Mood:** {emotion['market_mood']}")
                            top = " | ".join([f"{e['emotion']}({e['score']}%)" for e in emotion["top_emotions"]])
                            st.markdown(f"**Top Emotions:** {top}")

                st.markdown("---")
                st.subheader("Overall Summary")
                col1, col2, col3 = st.columns(3)
                col1.metric("Positive Headlines", positive_count)
                col2.metric("Negative Headlines", negative_count)
                col3.metric("Neutral Headlines",  neutral_count)

                overall = "POSITIVE" if positive_count > negative_count else "NEGATIVE" if negative_count > positive_count else "NEUTRAL"
                st.markdown(f"### Overall Sentiment -> **{overall}**")
    else:
        st.warning("Please enter a topic to analyze!")
