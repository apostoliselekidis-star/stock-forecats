import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'rf_model.joblib')


def _make_lag_features(s: pd.Series, nlags=10):
    df = pd.DataFrame({'y': s.values}, index=s.index)
    for i in range(1, nlags+1):
        df[f'lag_{i}'] = df['y'].shift(i)
    df = df.dropna()
    return df


def _get_news_sentiment(ticker: str):
    # Placeholder: no external requests to news provider to keep offline-friendly.
    # Return zeros which means no sentiment data available.
    return None


def train_and_forecast(series: pd.Series, days=7, retrain=False):
    # series: indexed series of close prices
    s = series.squeeze() if hasattr(series, 'squeeze') else series
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    s = s.dropna()
    if len(s) < 30:
        return None, None

    nlags = 10
    df = _make_lag_features(s, nlags=nlags)
    X = df[[f'lag_{i}' for i in range(1, nlags+1)]].values
    y = df['y'].values

    model = None
    if os.path.exists(MODEL_PATH) and not retrain:
        try:
            model = joblib.load(MODEL_PATH)
        except Exception:
            model = None

    if model is None:
        model = RandomForestRegressor(n_estimators=200, random_state=42)
        tscv = TimeSeriesSplit(n_splits=3)
        # quick training
        model.fit(X, y)
        try:
            joblib.dump(model, MODEL_PATH)
        except Exception:
            pass

    # iterative forecasting
    last_window = s.values[-nlags:]
    preds = []
    for _ in range(days):
        x = last_window[::-1]  # lag_1 is most recent
        x = x.reshape(1, -1)
        p = model.predict(x)[0]
        preds.append(p)
        last_window = np.append(last_window[1:], p)

    return model, np.array(preds)
