# Setup Guide for Stock Analyzer

## Prerequisites
- Windows with PowerShell
- Python 3.9+ installed

## Step 1: Install Dependencies

```powershell
cd "C:\Users\Tolaros\Desktop\Stock forecats"
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Step 2: (Optional) Configure News API

To use live market news sentiment:

1. Sign up at [NewsAPI.org](https://newsapi.org/) (free plan available)
2. Copy your API key
3. Set it in PowerShell:
   ```powershell
   $env:NEWSAPI_KEY = "your-api-key-here"
   ```
4. Restart the app to use news sentiment

Without API key, the app uses demo sentiment data.

## Step 3: Run the App

```powershell
cd "C:\Users\Tolaros\Desktop\Stock forecats"
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8503`

## Step 4: Using the App

### Sidebar Controls
- **Ticker**: Enter stock symbol (AAPL, MSFT, TSLA, etc.)
- **Time Period**: 1 Day, 1 Month, 6 Months, 1 Year, 5 Years
- **Forecast Days**: How many days to predict (1-90)
- **Forecast Model**: RandomForest (recommended), ARIMA, or LSTM
- **Advanced Settings**: Tweak lag features, sentiment, backtest %

### Main Features
- **Blue Price Line** — Daily closing price
- **Orange/Red Lines** — SMA 50 and SMA 200 moving averages
- **Green Dashed Line** — ML forecast
- **Trading Signal Card** — BUY/SELL/HOLD recommendation
- **Backtest Metrics** — Model accuracy on recent data
- **Fair Price Estimate** — Multi-method valuation

## Troubleshooting

### App won't start
- Ensure Python and pip are in PATH: `python --version`
- Reinstall packages: `pip install -r requirements.txt --force-reinstall`

### Chart not showing
- Try different time period (1 Year works best)
- Check browser console (F12) for errors

### News sentiment not working
- Requires `$env:NEWSAPI_KEY` to be set
- Check that API key is valid
- App uses demo data as fallback

### Slow performance
- Reduce Time Period to 1 Month or 6 Months
- Reduce Lag Features to 5-10
- Reduce Backtest % to 10-15%

## Data Sources
- **Prices**: yfinance (Yahoo Finance)
- **News**: NewsAPI.org (if enabled)
- **Fundamentals**: yfinance

## Key Metrics Explained

### Forecast Metrics
- **RMSE**: Average prediction error in dollars (lower is better)
- **MAE**: Mean absolute error (lower is better)
- **Direction Accuracy**: % of times model predicted correct direction

### Trading Signals
- **BUY**: RSI < 30 (oversold) AND Price > SMA 50
- **SELL**: RSI > 70 (overbought) OR Price < SMA 200
- **HOLD**: No strong signal

### Fair Price Methods
- **P/E Multiple**: Based on earnings valuation
- **Gordon Growth**: Dividend discount model
- **DCF**: Discounted cash flow analysis
- **Price-to-Book**: Book value adjusted for sector

## Support

For issues or questions:
1. Check the README.md for feature details
2. Review the Limitations section — some issues are known
3. Ensure all Python packages are installed: `pip list`

Enjoy analyzing stocks! 📈
