# Quick Start Cheatsheet

## Start the App (One Line)
```powershell
cd "C:\Users\Tolaros\Desktop\Stock forecats" ; streamlit run app.py
```

Open browser: `http://localhost:8503`

---

## Default Settings
```
Ticker:           AAPL
Time Period:      1 Year
Forecast Days:    7
Model:            RandomForest
Lag Features:     10
Sentiment:        ON
Backtest %:       20%
```

---

## Key Controls

### Sidebar
1. **Type Ticker** — Enter any stock symbol (AAPL, MSFT, TSLA, BRK.B, etc.)
2. **Select Period** — 1D, 1M, 6M, 1Y, 5Y
3. **Set Forecast Days** — 1-90 days ahead
4. **Choose Model** — RandomForest (recommended), ARIMA, LSTM
5. **Advanced Settings** ▼
   - **Lag Features** — 5-30 (higher = more complex, slower)
   - **Include Sentiment** — ON/OFF (requires NewsAPI key for live)
   - **Backtest %** — 5-50% (5% = conservative, 50% = aggressive)
6. **Retrain Button** — Force model retraining

---

## Chart Legend
```
Blue Line          → Close Price (main indicator)
Orange Line        → SMA 50 (intermediate trend)
Red Line           → SMA 200 (long-term trend)
Green Dashed Line  → ML Forecast (predicted future)
```

---

## Trading Signals
```
🟢 BUY    When: RSI < 30 AND Price > SMA50
🔴 SELL   When: RSI > 70 OR Price < SMA200
⚪ HOLD    Otherwise (no clear signal)
```

---

## Key Metrics Explained

### Forecast Performance (Below Chart)
- **RMSE** — Prediction error (lower = better). E.g., $2.50 = average $2.50 error
- **MAE** — Mean absolute error (easier to interpret)
- **Direction Accuracy** — % times model predicted correct direction
- **Test Periods** — Days used to validate model

### Valuation
- **P/E Ratio** — Stock price ÷ earnings per share
- **Fair Price** — Estimated intrinsic value
- **Upside/Downside** — % gain/loss if stock reaches fair price
- **Methods** — P/E Multiple, Gordon Growth, DCF, Price-to-Book

### Technical Indicators
- **RSI (0-100)** — <30=Oversold, >70=Overbought
- **MACD** — Momentum indicator
- **Bollinger Bands** — Volatility & support/resistance
- **SMA** — Trend direction

---

## Best Practices

### For Accuracy
- ✅ Use 1 Year (default) or 6 Months data
- ✅ Set forecast days = 5-30 (not too far ahead)
- ✅ Check backtest metrics (direction accuracy > 50%)
- ✅ Use sentiment toggle ON for better features
- ✅ Reduce to 1 Month if data is sparse

### For Speed
- ✅ Use 1 Month or 6 Months period
- ✅ Reduce lag features to 5-10
- ✅ Turn sentiment OFF (if slow)
- ✅ Use RandomForest model (ARIMA/LSTM are slower)

### For Analysis
- ✅ Compare multiple tickers side-by-side
- ✅ Check fundamentals tab (P/E vs peers)
- ✅ Note trading signals (but verify with other data)
- ✅ Review backtest accuracy before trusting forecast

---

## Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| Chart is empty | Try 1 Year period, different ticker |
| Slow performance | Reduce lag features to 5, turn off sentiment |
| News sentiment not showing | Set `$env:NEWSAPI_KEY` before running |
| Model not retraining | Click "Retrain" button, or adjust settings |
| Invalid ticker | Check spelling (e.g., AAPL not APPLE) |
| Low direction accuracy | Stock may be random; forecast less reliable |

---

## Ticker Examples

### Mega Cap (Most Stable)
- **AAPL** — Apple
- **MSFT** — Microsoft
- **GOOGL** — Google
- **AMZN** — Amazon
- **NVDA** — NVIDIA

### Growth
- **TSLA** — Tesla
- **META** — Meta (Facebook)
- **NFLX** — Netflix
- **PYPL** — PayPal

### Dividends
- **JNJ** — Johnson & Johnson
- **PG** — Procter & Gamble
- **KO** — Coca-Cola
- **CSCO** — Cisco

### ETFs
- **SPY** — S&P 500
- **QQQ** — Nasdaq 100
- **IWM** — Russell 2000

---

## Command Line Tips

### Set API Key (Windows)
```powershell
# Temporary (session only)
$env:NEWSAPI_KEY = "sk_live_xxxxx"

# Permanent (system-wide)
[Environment]::SetEnvironmentVariable("NEWSAPI_KEY", "sk_live_xxxxx", "User")
```

### Verify Installation
```powershell
python -c "import streamlit; print('✅ Streamlit installed')"
python -c "import yfinance; print('✅ yfinance installed')"
python -c "import sklearn; print('✅ scikit-learn installed')"
```

### Update Packages
```powershell
pip install --upgrade -r requirements.txt
```

---

## Key Files to Know

```
app.py                — Main application (run this)
utils/news.py         — News & sentiment
utils/forecast_v2.py  — ML models & backtesting
utils/valuation.py    — Fair price estimation
README.md             — Full documentation
SETUP_GUIDE.md        — Installation help
```

---

## Keyboard Shortcuts (Browser)

```
F12         → Open browser console (debug)
Ctrl+R      → Refresh app
Ctrl+Shift+I → Browser dev tools
```

---

## Useful Resources

- **yfinance Docs**: https://github.com/ranaroussi/yfinance
- **Streamlit Docs**: https://docs.streamlit.io
- **NewsAPI Docs**: https://newsapi.org/docs
- **VADER Sentiment**: https://github.com/cjhutto/vaderSentiment
- **scikit-learn**: https://scikit-learn.org

---

## Support

1. Check **README.md** for features
2. Check **SETUP_GUIDE.md** for installation
3. Check **FEATURES.md** for detailed checklist
4. Check **COMPLETION_REPORT.md** for architecture

---

## One-Minute Tutorial

1. **Start** the app:
   ```powershell
   streamlit run app.py
   ```

2. **Enter** a ticker (AAPL)

3. **View** the blue price line on chart

4. **Check** the 🟢 BUY / 🔴 SELL signal

5. **Read** "Fair Price" to see valuation

6. **Review** backtest metrics (accuracy > 50% = good)

7. **Adjust** settings and rerun

Done! 📊

---

**Last Updated**: January 31, 2026
