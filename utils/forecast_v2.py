"""
ML-based price forecasting with multiple models and backtesting
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import warnings

warnings.filterwarnings('ignore')


def create_lag_features(data, nlags=10):
    """
    Create lag features from time series data
    
    Args:
        data: Series of price data
        nlags: Number of lags to create
    
    Returns:
        X: Feature matrix with lag values
        y: Target variable (next day's price)
    """
    X, y = [], []
    
    # Ensure we have a numpy array
    prices = np.array(data).flatten()
    
    for i in range(len(prices) - nlags - 1):
        # Create lag features
        lags = prices[i:i+nlags]
        next_price = prices[i+nlags+1]
        
        X.append(lags)
        y.append(next_price)
    
    return np.array(X), np.array(y)


def add_sentiment_feature(X, sentiment_series=None):
    """
    Add sentiment as additional feature if available
    
    Args:
        X: Feature matrix
        sentiment_series: Series of sentiment scores
    
    Returns:
        X_augmented: Feature matrix with sentiment column
    """
    if sentiment_series is None or len(sentiment_series) == 0:
        return X
    
    # Ensure sentiment_series aligns with X
    sentiment_values = np.array(sentiment_series).flatten()
    
    # If sentiment is shorter, pad it
    if len(sentiment_values) < len(X):
        sentiment_values = np.pad(
            sentiment_values, 
            (0, len(X) - len(sentiment_values)), 
            mode='constant', 
            constant_values=0
        )
    else:
        sentiment_values = sentiment_values[:len(X)]
    
    # Add sentiment as last feature
    X_augmented = np.column_stack([X, sentiment_values])
    return X_augmented


def train_model(X_train, y_train, model_type="rf"):
    """
    Train a forecasting model
    
    Args:
        X_train: Training features
        y_train: Training targets
        model_type: Type of model ("rf", "arima", "lstm")
    
    Returns:
        Trained model object
    """
    if model_type == "rf" or model_type == "randomforest":
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=1,  # Single-threaded to avoid joblib issues
            min_samples_split=5,
            min_samples_leaf=2
        )
        model.fit(X_train, y_train)
        return model
    
    # For ARIMA and LSTM, use simplified RandomForest as fallback
    # (Full implementations would require statsmodels and keras)
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=1,  # Single-threaded to avoid joblib issues
        min_samples_split=5,
        min_samples_leaf=2
    )
    model.fit(X_train, y_train)
    return model


def forecast_prices(model, last_values, num_days, nlags=10, use_sentiment=False):
    """
    Generate future price forecasts
    
    Args:
        model: Trained model
        last_values: Last nlags price values from historical data
        num_days: Number of days to forecast
        nlags: Number of lag features used in training
        use_sentiment: Deprecated parameter, kept for compatibility
    
    Returns:
        Array of forecasted prices
    """
    predictions = []
    current_lags = np.array(last_values[-nlags:]).flatten()
    
    for _ in range(num_days):
        # Prepare input for next prediction
        X_next = current_lags.reshape(1, -1)
        
        next_price = model.predict(X_next)[0]
        
        # Ensure price is positive and reasonable
        next_price = max(next_price, current_lags[-1] * 0.5)  # Can't drop more than 50%
        next_price = min(next_price, current_lags[-1] * 1.5)  # Can't jump more than 50%
        
        predictions.append(next_price)
        
        # Update lags with new prediction
        current_lags = np.append(current_lags[1:], next_price)
    
    return np.array(predictions)


def backtest_model(X, y, nlags=10, test_size=0.2, model_type="rf"):
    """
    Walk-forward backtesting of the model
    
    Args:
        X: Feature matrix
        y: Target values
        nlags: Number of lag features
        test_size: Proportion for test set
        model_type: Type of model
    
    Returns:
        Dictionary with backtest metrics
    """
    test_periods = max(1, int(len(X) * test_size))
    train_size = len(X) - test_periods
    
    X_train = X[:train_size]
    y_train = y[:train_size]
    X_test = X[train_size:]
    y_test = y[train_size:]
    
    # Train model
    model = train_model(X_train, y_train, model_type)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = np.mean(np.abs(y_pred - y_test))
    rmse = np.sqrt(np.mean((y_pred - y_test) ** 2))
    
    # Direction accuracy: did we get the direction right?
    actual_direction = np.diff(y_test) > 0
    pred_direction = np.diff(y_pred) > 0
    direction_accuracy = np.mean(actual_direction == pred_direction) if len(actual_direction) > 0 else 0.5
    
    return {
        'rmse': float(rmse),
        'mae': float(mae),
        'direction_accuracy': float(direction_accuracy),
        'test_periods': int(test_periods),
        'train_size': int(train_size),
        'model': model
    }


def train_and_forecast(close_prices, days=7, retrain=False, model_type="rf", 
                      sentiment=None, nlags=10, test_size=0.2):
    """
    Main function: Train model and produce forecast
    
    Args:
        close_prices: Series of historical close prices
        days: Number of days to forecast
        retrain: Force retraining (ignore cache)
        model_type: Type of model to use
        sentiment: Optional sentiment series (currently not used to avoid feature mismatch)
        nlags: Number of lag features
        test_size: Backtest test set proportion
    
    Returns:
        Tuple: (model, forecast_prices, backtest_metrics)
    """
    try:
        # Ensure close_prices is a numpy array
        prices = np.array(close_prices).flatten()
        
        if len(prices) < nlags + 10:
            # Not enough data
            return None, None, {}
        
        # Create features and targets from price lags only
        # (sentiment causes feature mismatch issues in forecasting)
        X, y = create_lag_features(prices, nlags=nlags)
        
        # Backtest to get metrics
        backtest_results = backtest_model(X, y, nlags=nlags, test_size=test_size, model_type=model_type)
        model = backtest_results['model']
        
        # Generate forecast using all available data
        X_all, y_all = create_lag_features(prices, nlags=nlags)
        
        model = train_model(X_all, y_all, model_type)
        
        # Forecast future prices
        last_values = prices[-nlags:]
        forecast = forecast_prices(model, last_values, days, nlags=nlags)
        
        return model, forecast, backtest_results
    
    except Exception as e:
        print(f"Error in forecast: {e}")
        return None, None, {}
