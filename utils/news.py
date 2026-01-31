"""
News fetching and sentiment analysis module
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# NewsAPI key - using free tier
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', 'demo')


def fetch_news_sentiment(ticker, days=7):
    """
    Fetch recent news articles for a stock ticker
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        days: Number of days to look back
    
    Returns:
        DataFrame with columns: title, description, url, source, date, sentiment
    """
    try:
        # Calculate date range
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        to_date = datetime.now().strftime('%Y-%m-%d')
        
        # Build query - search for company news
        query = f"{ticker} stock OR {ticker} earnings OR {ticker} merger"
        
        # Try NewsAPI
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': query,
            'from': from_date,
            'to': to_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': NEWSAPI_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            if not articles:
                return None
            
            # Parse articles
            news_list = []
            for article in articles[:20]:  # Limit to 20 articles
                try:
                    news_list.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'date': article.get('publishedAt', ''),
                        'sentiment': analyze_sentiment(article.get('title', '') + ' ' + article.get('description', ''))
                    })
                except:
                    continue
            
            if news_list:
                df = pd.DataFrame(news_list)
                df['date'] = pd.to_datetime(df['date']).dt.date
                return df
        
        return None
    
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None


def analyze_sentiment(text):
    """
    Simple sentiment analysis using keyword matching
    Returns a score between -1 and 1
    """
    if not text:
        return 0
    
    text_lower = text.lower()
    
    # Positive keywords
    positive = ['gain', 'rally', 'surge', 'jump', 'soar', 'bull', 'bullish', 
                'strong', 'excellent', 'great', 'buy', 'upgrade', 'outperform',
                'beat', 'profit', 'growth', 'success', 'rise', 'up']
    
    # Negative keywords
    negative = ['loss', 'fall', 'crash', 'plunge', 'bear', 'bearish', 'weak',
                'poor', 'sell', 'downgrade', 'underperform', 'miss', 'loss',
                'decline', 'down', 'cut', 'warning', 'risk']
    
    # Count occurrences
    positive_count = sum(1 for word in positive if word in text_lower)
    negative_count = sum(1 for word in negative if word in text_lower)
    
    # Calculate sentiment
    if positive_count + negative_count == 0:
        return 0
    
    sentiment = (positive_count - negative_count) / (positive_count + negative_count)
    return max(-1, min(1, sentiment))  # Clamp to [-1, 1]


def get_top_headlines(ticker, limit=5):
    """
    Get top headlines for a ticker
    
    Args:
        ticker: Stock ticker symbol
        limit: Number of headlines to return
    
    Returns:
        List of headlines with metadata
    """
    try:
        df = fetch_news_sentiment(ticker, days=7)
        
        if df is None or df.empty:
            return []
        
        # Sort by date and sentiment (recent + positive first)
        df = df.sort_values('date', ascending=False)
        
        headlines = []
        for idx, row in df.head(limit).iterrows():
            headlines.append({
                'title': row['title'],
                'source': row['source'],
                'date': row['date'],
                'sentiment': row['sentiment'],
                'url': row['url'],
                'description': row['description']
            })
        
        return headlines
    
    except Exception as e:
        print(f"Error getting headlines: {e}")
        return []


def aggregate_sentiment_features(news_df):
    """
    Create features from news for ML model
    
    Args:
        news_df: DataFrame from fetch_news_sentiment
    
    Returns:
        Dictionary with sentiment features
    """
    try:
        if news_df is None or news_df.empty:
            return {
                'avg_sentiment': 0,
                'positive_pct': 0,
                'article_count': 0,
                'latest_sentiment': 0
            }
        
        sentiments = news_df['sentiment'].values
        positive = (sentiments > 0.1).sum()
        total = len(sentiments)
        
        return {
            'avg_sentiment': float(sentiments.mean()),
            'positive_pct': positive / total if total > 0 else 0,
            'article_count': total,
            'latest_sentiment': float(sentiments[0]) if len(sentiments) > 0 else 0
        }
    
    except Exception as e:
        print(f"Error aggregating sentiment: {e}")
        return {
            'avg_sentiment': 0,
            'positive_pct': 0,
            'article_count': 0,
            'latest_sentiment': 0
        }
