import yfinance as yf


def get_fundamentals(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    info = t.info if hasattr(t, 'info') else {}

    fundamentals = {
        'shortName': info.get('shortName'),
        'marketCap': info.get('marketCap'),
        'trailingPE': info.get('trailingPE'),
        'forwardPE': info.get('forwardPE'),
        'priceToBook': info.get('priceToBook'),
        'dividendYield': info.get('dividendYield') or info.get('dividendYield'),
        'beta': info.get('beta')
    }
    return fundamentals
