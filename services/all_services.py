
import os
import requests
import yfinance as yf
from transformers import pipeline
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load all models
finbert       = pipeline("sentiment-analysis", model="ProsusAI/finbert")
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
fear_greed_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# API keys
gnews_key = os.environ.get("GNEWS_API_KEY")
newsapi   = NewsApiClient(api_key=os.environ.get("NEWS_API_KEY"))

def fetch_all_news(query, max_results=5):
    try:
        gnews_response = requests.get(
            "https://gnews.io/api/v4/search",
            params={"q": query, "lang": "en", "max": max_results, "apikey": gnews_key}
        )
        gnews_headlines = [a["title"] for a in gnews_response.json().get("articles", [])]
    except:
        gnews_headlines = []

    try:
        newsapi_results  = newsapi.get_everything(q=query, language="en", sort_by="relevancy", page_size=max_results)
        newsapi_headlines = [a["title"] for a in newsapi_results["articles"]]
    except:
        newsapi_headlines = []

    all_headlines = list(set(gnews_headlines + newsapi_headlines))
    return all_headlines

def analyze_sentiment(text):
    result = finbert(text[:512])[0]
    label  = result["label"].upper()
    score  = round(result["score"] * 100, 1)
    signal = "BULLISH" if label == "POSITIVE" else "BEARISH" if label == "NEGATIVE" else "NEUTRAL"
    return {"sentiment": label, "confidence": score, "signal": signal}

def detect_emotion(text):
    results        = emotion_model(text[:512])[0]
    sorted_emotions = sorted(results, key=lambda x: x["score"], reverse=True)
    top_emotions   = [{"emotion": e["label"].upper(), "score": round(e["score"] * 100, 1)} for e in sorted_emotions[:3]]
    primary        = top_emotions[0]["emotion"]
    fear_emotions  = ["FEAR", "DISGUST", "ANGER", "SADNESS"]
    market_mood    = "FEAR" if primary in fear_emotions else "GREED"
    return {"top_emotions": top_emotions, "primary": primary, "market_mood": market_mood}

def calculate_fear_greed(headlines):
    labels    = ["extreme fear", "fear", "neutral", "greed", "extreme greed"]
    score_map = {"extreme fear": 10, "fear": 30, "neutral": 50, "greed": 75, "extreme greed": 95}
    total     = 0
    for headline in headlines:
        result = fear_greed_model(headline[:512], candidate_labels=labels)
        total += score_map[result["labels"][0]]
    final_score = round(total / len(headlines))
    if final_score <= 20:   meter = "EXTREME FEAR"
    elif final_score <= 40: meter = "FEAR"
    elif final_score <= 60: meter = "NEUTRAL"
    elif final_score <= 80: meter = "GREED"
    else:                   meter = "EXTREME GREED"
    return {"score": final_score, "meter": meter}

def fetch_stock_data(ticker):
    stock     = yf.Ticker(ticker)
    info      = stock.fast_info
    hist      = stock.history(period="5d")
    price     = round(info.last_price, 2)
    prev      = info.previous_close
    change    = round(((price - prev) / prev) * 100, 2)
    trend     = "UPWARD" if hist["Close"].iloc[-1] > hist["Close"].iloc[0] else "DOWNWARD"
    direction = "UP" if change > 0 else "DOWN"
    return {"ticker": ticker, "price": price, "change": change, "trend": trend, "direction": direction}
