import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
from utils.indicators import add_technical_indicators
from utils.fundamentals import get_fundamentals
from utils.valuation import estimate_fair_price
from utils.forecast_v2 import train_and_forecast
from utils.signals import generate_signals, get_latest_signal
from utils.news import fetch_news_sentiment, aggregate_sentiment_features
from utils.scoring import generate_complete_score

st.set_page_config(layout="wide", page_title="Stock Analyzer")

st.title("Stock Analyzer & Forecaster")

with st.sidebar:
    st.header("Stock Analysis Settings")
    ticker = st.text_input("Ticker (e.g. AAPL)", value="AAPL").upper().strip()
    
    # Time period selection with better options
    period_options = {
        "1 Day": ("1d", "1h"),
        "1 Month": ("1mo", "1d"),
        "6 Months": ("6mo", "1d"),
        "1 Year": ("1y", "1d"),
        "5 Years": ("5y", "1wk")
    }
    selected_period = st.selectbox("Time Period", list(period_options.keys()), index=3)
    period, interval = period_options[selected_period]
    
    st.divider()
    st.subheader("Forecast Settings")
    forecast_days = st.slider("Forecast Days", min_value=1, max_value=90, value=7, step=1)
    
    # Model selection
    model_type = st.selectbox("Forecast Model", ["RandomForest", "ARIMA", "LSTM"], index=0)
    model_type_map = {"RandomForest": "rf", "ARIMA": "arima", "LSTM": "lstm"}
    selected_model = model_type_map[model_type]
    
    # Advanced options
    with st.expander("Advanced Settings"):
        nlags = st.slider("Lag Features", min_value=5, max_value=30, value=10, step=1)
        use_sentiment = st.checkbox("Include News Sentiment", value=True)
        test_size = st.slider("Backtest % (test data)", min_value=5, max_value=50, value=20, step=5)
    
    retrain = st.button("🔄 Retrain Forecast Model")

if not ticker:
    st.info("Enter a ticker symbol in the sidebar.")
    st.stop()

@st.cache_data
def load_data(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    data.index = pd.to_datetime(data.index)
    return data

with st.spinner("Fetching data..."):
    df = load_data(ticker, period, interval)

if df.empty:
    st.error("No data found for ticker. Check the symbol and try again.")
    st.stop()

# Fetch news sentiment if enabled
df_news = None
sentiment_series = None
if use_sentiment:
    with st.spinner("Fetching news sentiment..."):
        try:
            df_news = fetch_news_sentiment(ticker, days=60)
            if df_news is not None and not df_news.empty:
                sentiment_series = pd.Series(df_news['sentiment'].values, index=df_news['date'])
        except Exception as e:
            st.warning(f"Could not fetch news sentiment: {e}")

st.subheader(f"Price chart for {ticker}")

fig = go.Figure()

# Extract close price data safely
close_prices = df['Close'].values
if isinstance(close_prices, np.ndarray):
    close_prices = close_prices.flatten()

# Add a bright blue line for price
fig.add_trace(go.Scatter(
    x=df.index,
    y=close_prices,
    mode='lines',
    name='Close Price',
    line=dict(color='blue', width=3)
))

# indicators
with st.spinner("Computing indicators..."):
    df_ind = add_technical_indicators(df.copy())
    df_ind = generate_signals(df_ind)

# overlay moving averages
if 'SMA_50' in df_ind.columns:
    sma50_data = df_ind['SMA_50'].values
    fig.add_trace(go.Scatter(
        x=df_ind.index, 
        y=sma50_data, 
        mode='lines', 
        name='SMA 50',
        line=dict(color='orange', width=2)
    ))

if 'SMA_200' in df_ind.columns:
    sma200_data = df_ind['SMA_200'].values
    fig.add_trace(go.Scatter(
        x=df_ind.index, 
        y=sma200_data, 
        mode='lines', 
        name='SMA 200',
        line=dict(color='red', width=2)
    ))

# Train and forecast
forecast = None
backtest_metrics = {}
with st.spinner(f"Training {model_type} model and producing forecast..."):
    model, forecast, backtest_metrics = train_and_forecast(
        df_ind['Close'].ffill(), 
        days=forecast_days, 
        retrain=retrain,
        model_type=selected_model,
        sentiment=sentiment_series,
        nlags=nlags,
        test_size=test_size/100.0
    )

if forecast is not None and len(forecast) > 0:
    fc_x = pd.date_range(start=df.index[-1], periods=len(forecast)+1, inclusive='right')
    forecast_data = np.array(forecast)
    fig.add_trace(go.Scatter(
        x=fc_x, 
        y=forecast_data, 
        mode='lines+markers', 
        name=f'Forecast ({forecast_days}d)', 
        line=dict(dash='dash', color='green', width=2),
        marker=dict(size=4)
    ))

fig.update_layout(
    xaxis_rangeslider_visible=False, 
    height=600,
    hovermode='x unified',
    title_text=f'{ticker} - Price & Technical Analysis',
    template='plotly_white',
    yaxis_title='Price ($)',
    xaxis_title='Date',
    yaxis=dict(autorange=True),
    margin=dict(l=50, r=50, t=50, b=50)
)
st.plotly_chart(fig, use_container_width='stretch')

# Fetch fundamentals first (needed for scoring)
st.subheader("Fundamentals & Valuation")
with st.spinner("Fetching fundamentals..."):
    fundamentals = get_fundamentals(ticker)

# Calculate comprehensive scoring AFTER fundamentals are loaded
with st.spinner("Calculating confidence scores..."):
    try:
        # Get current price
        current_price = df_ind['Close'].iloc[-1]
        if isinstance(current_price, pd.Series):
            current_price = current_price.iloc[0] if len(current_price) > 0 else current_price.values[0]
        current_price = float(current_price)
        
        # Prepare sentiment data
        sentiment_data = {}
        if sentiment_series is not None and len(sentiment_series) > 0:
            # Safely get recent articles if available
            recent_articles = []
            if df_news is not None and not df_news.empty:
                try:
                    # Try to get title and sentiment columns
                    if 'title' in df_news.columns and 'sentiment' in df_news.columns:
                        recent_articles = df_news[['title', 'sentiment']].head(5).to_dict('records')
                    elif 'title' in df_news.columns:
                        recent_articles = df_news[['title']].head(5).to_dict('records')
                except:
                    recent_articles = []
            
            sentiment_data = {
                'daily_sentiment': float(sentiment_series.iloc[-1]) if len(sentiment_series) > 0 else 0,
                'recent_articles': recent_articles
            }
        
        # Generate scoring
        score_result = generate_complete_score(
            ticker=ticker,
            indicators_df=df_ind,
            current_price=current_price,
            fundamentals=fundamentals,
            backtest_metrics=backtest_metrics,
            sentiment_data=sentiment_data
        )
    except Exception as e:
        st.warning(f"Could not calculate scores: {e}")
        score_result = None

# Display comprehensive recommendation card
if score_result:
    summary = score_result['summary']
    
    # Main recommendation card with color coding
    if summary['recommendation'] == 'STRONG BUY':
        card_color = '#90EE90'  # Light green
    elif summary['recommendation'] == 'BUY':
        card_color = '#98FB98'  # Pale green
    elif summary['recommendation'] == 'HOLD':
        card_color = '#FFFACD'  # Light yellow
    elif summary['recommendation'] == 'SELL':
        card_color = '#FFB6C6'  # Light red
    else:
        card_color = '#FF6B6B'  # Red
    
    st.markdown(f"""
    <div style="background-color: {card_color}; padding: 20px; border-radius: 10px; border: 2px solid black; margin: 10px 0;">
        <h2 style="margin: 0; text-align: center;">{summary['emoji']} {summary['recommendation']}</h2>
        <h4 style="margin: 10px 0; text-align: center;">{summary['description']}</h4>
        <div style="display: flex; justify-content: space-around; margin-top: 15px;">
            <div style="text-align: center;">
                <p style="font-size: 24px; font-weight: bold; margin: 0;">{summary['score']:.1f}/10</p>
                <p style="margin: 5px 0; font-size: 12px;">Overall Score</p>
            </div>
            <div style="text-align: center;">
                <p style="font-size: 24px; font-weight: bold; margin: 0;">${current_price:.2f}</p>
                <p style="margin: 5px 0; font-size: 12px;">Current Price</p>
            </div>
            <div style="text-align: center;">
                <p style="font-size: 24px; font-weight: bold; margin: 0;">{summary['risk_level']}</p>
                <p style="margin: 5px 0; font-size: 12px;">Risk Level</p>
            </div>
            <div style="text-align: center;">
                <p style="font-size: 24px; font-weight: bold; margin: 0;">{summary['confidence']}</p>
                <p style="margin: 5px 0; font-size: 12px;">Confidence</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Score breakdown in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Technical", "💼 Fundamental", "🤖 Forecast", "📰 Sentiment"])
    
    with tab1:
        tech = score_result['technical']
        st.metric("Technical Score", f"{tech['score']:.1f}/10")
        st.write(f"**Analysis:** {tech['reasoning']}")
        st.write("**Component Breakdown:**")
        
        tech_cols = st.columns(min(5, len(tech['components'])))
        for idx, (component_name, component_data) in enumerate(tech['components'].items()):
            with tech_cols[idx % len(tech_cols)]:
                score_val = component_data['score']
                color = '🟢' if score_val > 6 else '🟡' if score_val > 4 else '🔴'
                st.write(f"{color} **{component_name.upper()}**")
                st.write(f"Score: {score_val:.1f}")
                st.caption(component_data['reason'])
    
    with tab2:
        fund = score_result['fundamental']
        st.metric("Fundamental Score", f"{fund['score']:.1f}/10")
        st.write(f"**Analysis:** {fund['reasoning']}")
        st.write("**Component Breakdown:**")
        
        fund_cols = st.columns(min(4, len(fund['components'])))
        for idx, (component_name, component_data) in enumerate(fund['components'].items()):
            with fund_cols[idx % len(fund_cols)]:
                score_val = component_data['score']
                color = '🟢' if score_val > 6 else '🟡' if score_val > 4 else '🔴'
                st.write(f"{color} **{component_name.upper()}**")
                st.write(f"Score: {score_val:.1f}")
                st.caption(component_data['reason'])
    
    with tab3:
        fcst = score_result['forecast']
        st.metric("Forecast Confidence", f"{fcst['score']:.1f}/10 ({fcst['confidence']})")
        st.write(f"**Analysis:** {fcst['reasoning']}")
        st.write("**Backtest Metrics:**")
        
        fcst_cols = st.columns(min(3, len(fcst['components'])))
        for idx, (component_name, component_data) in enumerate(fcst['components'].items()):
            with fcst_cols[idx % len(fcst_cols)]:
                score_val = component_data['score']
                color = '🟢' if score_val > 6 else '🟡' if score_val > 4 else '🔴'
                st.write(f"{color} **{component_name.replace('_', ' ').upper()}**")
                st.write(f"Score: {score_val:.1f}")
                st.caption(component_data['reason'])
    
    with tab4:
        sent = score_result['sentiment']
        st.metric("Sentiment Score", f"{sent['score']:.1f}/10 ({sent['sentiment']})")
        st.write(f"**Analysis:** {sent['reasoning']}")
        
        if sent['articles']:
            st.write("**Recent News:**")
            for i, article in enumerate(sent['articles'], 1):
                emoji = '📈' if article.get('sentiment', 0) > 0.2 else '📉' if article.get('sentiment', 0) < -0.2 else '➡️'
                st.caption(f"{emoji} {article.get('title', 'Article')[:80]}...")
else:
    # Fallback to simple signal display
    signal = get_latest_signal(df_ind)
    col1, col2, col3 = st.columns(3)
    with col1:
        if signal == 'BUY':
            st.metric("Trading Signal", "🟢 BUY", delta="Oversold + Above SMA50")
        elif signal == 'SELL':
            st.metric("Trading Signal", "🔴 SELL", delta="Overbought or Below SMA200")
        else:
            st.metric("Trading Signal", "⚪ HOLD", delta="No clear signal")
    
    with col2:
        current_price = df_ind['Close'].iloc[-1]
        if isinstance(current_price, pd.Series):
            current_price = current_price.iloc[0] if len(current_price) > 0 else current_price.values[0]
        current_price = float(current_price)
        st.metric("Current Price", f"${current_price:.2f}")
    
    with col3:
        if 'SMA_50' in df_ind.columns:
            sma50 = df_ind['SMA_50'].iloc[-1]
            if isinstance(sma50, pd.Series):
                sma50 = sma50.iloc[0] if len(sma50) > 0 else sma50.values[0]
            sma50 = float(sma50)
            diff_pct = ((current_price - sma50) / sma50) * 100
            st.metric("vs SMA 50", f"${sma50:.2f}", delta=f"{diff_pct:+.2f}%")

st.divider()
valuation_result = estimate_fair_price(fundamentals, df_ind, ticker=ticker)
fair_price = valuation_result['fair_price']
upside = valuation_result['upside']
valuation_methods = valuation_result.get('methods', {})

col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Valuation Metrics**")
    if fundamentals.get('trailingPE'):
        st.metric("P/E Ratio (TTM)", f"{fundamentals['trailingPE']:.2f}")
    if fundamentals.get('forwardPE'):
        st.metric("Forward P/E", f"{fundamentals['forwardPE']:.2f}")

with col2:
    st.write("**Risk & Yield**")
    if fundamentals.get('beta'):
        st.metric("Beta", f"{fundamentals['beta']:.2f}")
    if fundamentals.get('dividendYield'):
        st.metric("Dividend Yield", f"{fundamentals['dividendYield']*100:.2f}%")

with col3:
    st.write("**Market Info**")
    if fundamentals.get('marketCap'):
        market_cap_b = fundamentals['marketCap'] / 1e9
        st.metric("Market Cap", f"${market_cap_b:.2f}B")

# Display valuation methods breakdown
if valuation_methods:
    st.write("**Valuation Method Breakdown:**")
    val_cols = st.columns(len(valuation_methods))
    for idx, (method_name, method_value) in enumerate(valuation_methods.items()):
        with val_cols[idx]:
            st.metric(method_name, f"${method_value:.2f}")

st.metric(
    "📊 Estimated Fair Price", 
    f"${fair_price:.2f}", 
    delta=f"{upside:+.2f}% upside" if upside > 0 else f"{upside:.2f}% downside"
)

# Backtesting metrics
if backtest_metrics and backtest_metrics.get('rmse'):
    st.subheader("Forecast Model Performance (Backtest)")
    btest_cols = st.columns(4)
    with btest_cols[0]:
        st.metric("RMSE", f"${backtest_metrics['rmse']:.2f}")
    with btest_cols[1]:
        st.metric("MAE", f"${backtest_metrics['mae']:.2f}")
    with btest_cols[2]:
        acc = backtest_metrics['direction_accuracy'] * 100
        st.metric("Direction Accuracy", f"{acc:.1f}%")
    with btest_cols[3]:
        st.metric("Test Periods", f"{backtest_metrics['test_periods']}")
    
    st.info(
        f"Model tested on {backtest_metrics['test_periods']} recent periods. "
        f"RMSE: ${backtest_metrics['rmse']:.2f}, "
        f"Direction accuracy: {acc:.1f}%"
    )

st.divider()
st.markdown("""
### Model Notes & Disclaimer
- **Forecast**: Trained on {nlags} lag features with sentiment analysis
- **Valuation**: Multi-method approach (P/E, Gordon Growth, DCF, P/B)
- **Signals**: Based on RSI (30/70) and SMA crossovers
- **Backtesting**: Walk-forward validation on recent {test_size}% of data
- ⚠️ **Disclaimer**: For educational purposes only. Not investment advice.
""".format(nlags=nlags, test_size=test_size))
