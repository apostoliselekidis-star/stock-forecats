import requests
import pandas as pd
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def fetch_news_sentiment(ticker: str, days: int = 30) -> pd.DataFrame:
    """
    Fetch recent news headlines for a stock and compute sentiment scores.
    Uses NewsAPI (free tier). Requires NEWSAPI_KEY environment variable.
    
    Returns DataFrame with columns: date, headline, sentiment_score
    """
    import os
    api_key = os.environ.get('NEWSAPI_KEY', 'demo')
    
    if api_key == 'demo':
        # Return dummy data for demo
        return _generate_dummy_sentiment(ticker, days)
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': ticker,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 100,
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return _generate_dummy_sentiment(ticker, days)
        
        data = response.json()
        articles = data.get('articles', [])
        
        news_list = []
        for article in articles:
            pub_date = article.get('publishedAt', '')
            headline = article.get('title', '')
            description = article.get('description', '')
            
            # Compute sentiment
            text = f"{headline} {description}"
            sentiment = analyzer.polarity_scores(text)
            
            try:
                date = pd.to_datetime(pub_date).date()
                news_list.append({
                    'date': date,
                    'headline': headline,
                    'sentiment_score': sentiment['compound']  # -1 to 1
                })
            except:
                pass
        
        if not news_list:
            return _generate_dummy_sentiment(ticker, days)
        
        df_news = pd.DataFrame(news_list)
        df_news['date'] = pd.to_datetime(df_news['date'])
        
        # Aggregate sentiment by date
        daily_sentiment = df_news.groupby('date')['sentiment_score'].mean().reset_index()
        daily_sentiment.columns = ['date', 'sentiment']
        
        return daily_sentiment
    
    except Exception as e:
        print(f"News fetch error: {e}")
        return _generate_dummy_sentiment(ticker, days)


def _generate_dummy_sentiment(ticker: str, days: int = 30) -> pd.DataFrame:
    """Generate dummy sentiment data for demo/offline mode."""
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days, freq='D')
    sentiment = [0.1 + (i % 10) * 0.05 for i in range(days)]  # Range 0.1 to 0.5
    return pd.DataFrame({'date': dates, 'sentiment': sentiment})


def aggregate_sentiment_features(df_price: pd.DataFrame, df_news: pd.DataFrame) -> pd.DataFrame:
    """
    Merge sentiment data into price dataframe as features.
    Fills missing dates with forward fill.
    """
    df_price = df_price.copy()
    df_price['date'] = df_price.index.date
    
    df_merged = df_price.merge(df_news, left_on='date', right_on='date', how='left')
    df_merged['sentiment'] = df_merged['sentiment'].fillna(method='ffill').fillna(0)
    
    return df_merged
