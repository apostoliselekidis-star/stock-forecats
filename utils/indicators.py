import pandas as pd
import numpy as np
import ta


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Ensure Close is 1D Series
    close = df['Close'].squeeze()
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    
    # SMA
    df['SMA_50'] = close.rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = close.rolling(window=200, min_periods=1).mean()

    # RSI
    try:
        rsi = ta.momentum.RSIIndicator(close, window=14)
        df['RSI_14'] = rsi.rsi()
    except Exception as e:
        # Fallback: compute RSI manually
        df['RSI_14'] = _compute_rsi(close, window=14)

    # MACD
    try:
        macd = ta.trend.MACD(close)
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
    except Exception as e:
        df['MACD'] = np.nan
        df['MACD_Signal'] = np.nan

    # Bollinger Bands
    try:
        bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
        df['BB_middle'] = bb.bollinger_mavg()
        df['BB_upper'] = bb.bollinger_hband()
        df['BB_lower'] = bb.bollinger_lband()
    except Exception as e:
        df['BB_middle'] = np.nan
        df['BB_upper'] = np.nan
        df['BB_lower'] = np.nan

    return df


def _compute_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
