import pandas as pd


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate buy/sell signals based on technical indicators.
    
    Strategy:
    - Buy signal: RSI < 30 (oversold) AND price above SMA 50
    - Sell signal: RSI > 70 (overbought) OR price below SMA 200
    - Hold/No Action: otherwise
    """
    df = df.copy()
    df['Signal'] = 'HOLD'
    
    # Ensure Close is a Series, not DataFrame
    close = df['Close'].squeeze()
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    
    # Ensure required columns exist
    has_rsi = 'RSI_14' in df.columns
    has_sma50 = 'SMA_50' in df.columns
    has_sma200 = 'SMA_200' in df.columns
    
    if has_rsi and has_sma50:
        # Buy: oversold (RSI < 30) and price above 50-day MA
        rsi = df['RSI_14'].squeeze()
        sma50 = df['SMA_50'].squeeze()
        buy_condition = (rsi < 30) & (close > sma50)
        df.loc[buy_condition, 'Signal'] = 'BUY'
    
    if has_rsi or has_sma200:
        # Sell: overbought (RSI > 70) or price below 200-day MA
        sell_condition = False
        if has_rsi:
            rsi = df['RSI_14'].squeeze()
            sell_condition = (rsi > 70)
        if has_sma200:
            sma200 = df['SMA_200'].squeeze()
            sell_condition = sell_condition | (close < sma200)
        df.loc[sell_condition, 'Signal'] = 'SELL'
    
    return df


def get_latest_signal(df: pd.DataFrame) -> str:
    """Get the most recent signal from the dataframe."""
    latest = df.iloc[-1]
    signal = latest.get('Signal', 'HOLD')
    # Ensure we return a scalar string, not a Series
    if isinstance(signal, pd.Series):
        signal = signal.iloc[0] if len(signal) > 0 else 'HOLD'
    return str(signal)
