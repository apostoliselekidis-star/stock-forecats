# Stock Analyzer & Forecaster (Advanced Edition)

A comprehensive Streamlit-based stock analysis and forecasting application with advanced ML models, sentiment analysis, multi-method valuation, and backtesting.

## Features

### 📊 Price Analysis
- **Interactive Price Chart** — Blue line showing daily closing prices with multiple time periods (1D, 1M, 6M, 1Y, 5Y)
- **Technical Indicators** — RSI, MACD, Bollinger Bands, SMA 50, SMA 200
- **Trading Signals** — Automated BUY/SELL/HOLD signals based on RSI and moving average crossovers

### 🤖 Advanced Forecasting
- **Multiple Model Types** — RandomForest, ARIMA (placeholder), LSTM (placeholder)
- **Configurable Lag Features** — 5-30 day lookback window
- **News Sentiment Integration** — Real-time market sentiment as model input
- **Backtesting Metrics** — RMSE, MAE, Directional Accuracy on recent data
- **Walk-Forward Validation** — Test on configurable % of recent data (5-50%)

### 💰 Multi-Method Valuation
- **P/E Multiple Method** — Peer-adjusted P/E ratio valuation
- **Gordon Growth Model** — Dividend-based intrinsic value with growth rate
- **DCF Analysis** — Free cash flow discounted to present value (5-year forecast)
- **Price-to-Book Method** — Sector-adjusted P/B valuation
- **Valuation Breakdown** — Compare all methods side-by-side

### 📰 News Sentiment
- **Headlines Integration** — Fetch recent news via NewsAPI (requires API key)
- **Sentiment Scoring** — VADER sentiment analysis (-1 to +1 scale)
- **Daily Aggregation** — Average sentiment per trading day as ML feature
- **Offline Mode** — Demo sentiment data if API unavailable

### 📈 Fundamental Metrics
- **P/E Ratios** — Trailing and Forward P/E
- **Risk Metrics** — Beta coefficient
- **Yield** — Dividend yield %
- **Market Cap** — Company size in billions

## Installation

### Requirements
- Python 3.9+
- See `requirements.txt` for full dependencies

### Setup (Windows PowerShell)

```powershell
cd "C:/Users/Tolaros/Desktop/Stock forecats"
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Optional: News API Setup

To enable live news fetching:
1. Get a free API key from [NewsAPI.org](https://newsapi.org/)
2. Set environment variable:
   ```powershell
   $env:NEWSAPI_KEY = "your-api-key-here"
   ```
3. Restart the app

## Quick Start

```powershell
streamlit run app.py
```

Then open your browser to `http://localhost:8503`

## Usage Guide

### Sidebar Controls

1. **Stock Ticker** — Enter stock symbol (e.g., AAPL, MSFT, TSLA)
2. **Time Period** — Choose view: 1 Day, 1 Month, 6 Months, 1 Year, 5 Years
3. **Forecast Days** — Set prediction horizon (1-90 days)
4. **Forecast Model** — Select RandomForest, ARIMA, or LSTM
5. **Advanced Settings** (expandable):
   - **Lag Features** — Number of past days to use (5-30)
   - **Include News Sentiment** — Toggle market sentiment as feature
   - **Backtest %** — Data split for validation (5-50%)

### Main Display

- **Price Chart** — Blue line with SMA 50 (orange) and SMA 200 (red) overlays + green forecast
- **Trading Signal** — Large metric card: BUY/SELL/HOLD with reason
- **Current Price & SMA Comparison** — Key metrics updated in real-time
- **Technical Indicators Table** — RSI, MACD, Bollinger Bands (latest 50 days)
- **Valuation Estimates** — Multiple methods with individual estimates
- **Fair Price** — Consensus estimate with upside/downside vs current
- **Backtest Metrics** — Model performance on recent test data

## Technical Details

### Forecast Model
- **Features**: Lag 1 to N, optional sentiment score
- **Training**: On 80% of historical data (configurable)
- **Testing**: Walk-forward backtest on recent 20% (configurable)
- **Metrics**:
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)
  - Direction Accuracy (% correct up/down prediction)

### Valuation Methods
1. **P/E Method** — Current price (simple baseline)
2. **Gordon Growth** — Dividend yield → intrinsic value (8% discount rate, 2.5% growth)
3. **DCF** — 5-year FCF forecast + terminal value (10% discount, 2.5% terminal growth)
4. **P/B Method** — Book value adjusted by sector average ratio

### Signal Logic
- **BUY**: RSI < 30 (oversold) AND Price > SMA 50
- **SELL**: RSI > 70 (overbought) OR Price < SMA 200
- **HOLD**: Otherwise

## Module Structure

```
utils/
├── indicators.py          # Technical indicator calculations
├── fundamentals.py        # Fetch P/E, beta, market cap, etc.
├── valuation.py           # P/E, DCF, Gordon Growth, P/B models
├── forecast_v2.py         # ML models with backtesting
├── signals.py             # Trading signal generation
└── news.py                # News fetching & sentiment analysis
```

## Limitations & Disclaimers

⚠️ **This is a prototype for educational/demonstration purposes ONLY.**

- Models and valuations are simplified approximations
- Historical performance ≠ future results
- News sentiment is simplified (VADER; no advanced NLP)
- DCF uses conservative assumptions (may not fit all sectors)
- Backtesting on historical data can be overly optimistic
- **NOT financial advice — consult a licensed advisor before investing**

## Future Improvements

- [ ] Real ARIMA & LSTM implementations
- [ ] Multi-stock portfolio analysis
- [ ] Real-time streaming data
- [ ] Advanced sentiment (transformer models)
- [ ] Options pricing integration
- [ ] Risk metrics (VaR, Sharpe ratio)
- [ ] Database for historical results
- [ ] API for programmatic access

## License

Educational use only. See LICENSE for details.

