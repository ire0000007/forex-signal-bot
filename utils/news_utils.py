# utils/news_utils.py

import requests
from datetime import datetime, timedelta
# utils/news_utils.py
import requests
from datetime import datetime, timedelta

# Replace with your real API key or disable this feature if you are testing
NEWS_API_KEY = 'pub_464f3c90ede34de29319fa1ad0423fa9'  # Leave as is if testing without news filter

def filter_news(symbol):
    """
    Checks for high-impact news for the given symbol in the next hour.
    Returns True if no major news, False if major news found.
    """
    try:
        # You can replace this with real API or mock data if testing
        if NEWS_API_KEY == 'YOUR_NEWS_API_KEY':
            print("⚠️ News check bypassed for testing.")
            return True

        url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        if response.status_code == 429:
            print("❌ News API Error: 429")
            return False

        data = response.json()
        articles = data.get("articles", [])
        now = datetime.utcnow()
        upcoming_hour = now + timedelta(hours=1)

        for article in articles:
            published = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            if now <= published <= upcoming_hour:
                print(f"❌ High-impact news detected for {symbol}: {article['title']}")
                return False

        print(f"✅ No major news found for {symbol}")
        return True

    except Exception as e:
        print(f"❌ News filter error: {str(e)}")
        return False

# Free News API (replace with your actual API key or use 'demo' for testing)
NEWS_API_KEY = "pub_464f3c90ede34de29319fa1ad0423fa9"
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Rate-limit tracking
last_request_time = None

def fetch_news_sentiment(symbol):
    """
    Fetch recent news for the symbol and return sentiment score (mocked for now).
    """
    global last_request_time
    try:
        # Rate limit: 1 request per minute
        if last_request_time and datetime.utcnow() - last_request_time < timedelta(seconds=60):
            print("❌ News API Error: Rate limit exceeded")
            return None, "rate_limit"

        params = {
            'q': symbol,
            'apiKey': NEWS_API_KEY,
            'sortBy': 'publishedAt',
            'pageSize': 5,
            'language': 'en'
        }
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        last_request_time = datetime.utcnow()

        if response.status_code == 200:
            articles = response.json().get('articles', [])
            if not articles:
                return "neutral", "no_articles"

            # Basic mock sentiment: keyword check (replace with real sentiment model if needed)
            sentiment_score = 0
            for article in articles:
                title = article['title'].lower()
                if "rise" in title or "bullish" in title:
                    sentiment_score += 1
                elif "fall" in title or "bearish" in title:
                    sentiment_score -= 1

            sentiment = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
            return sentiment, "ok"
        else:
            print(f"❌ News API Error: {response.status_code}")
            return None, "api_error"
    except Exception as e:
        print(f"❌ News API Exception: {e}")
        return None, "exception"
