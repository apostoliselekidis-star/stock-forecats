import numpy as np
import yfinance as yf


def estimate_fair_price(fundamentals: dict, df: object, ticker: str = None) -> dict:
    """
    Estimate fair price using multiple valuation methods.
    Returns dict with 'fair_price', 'valuation_methods', and breakdown.
    """
    prices = df['Close'].dropna()
    last_price = float(prices.iloc[-1]) if len(prices) > 0 else 100.0

    estimates = {}
    
    # 1. P/E-based valuation
    pe_estimate = _pe_valuation(fundamentals, last_price)
    if pe_estimate:
        estimates['P/E Multiple'] = pe_estimate
    
    # 2. Gordon Growth Model
    gg_estimate = _gordon_growth_valuation(fundamentals, last_price)
    if gg_estimate:
        estimates['Gordon Growth'] = gg_estimate
    
    # 3. Simple DCF (if we can get cash flow data)
    if ticker:
        dcf_estimate = _simple_dcf_valuation(ticker, last_price)
        if dcf_estimate:
            estimates['DCF (Simple)'] = dcf_estimate
    
    # 4. Price-to-Book
    pb_estimate = _price_to_book_valuation(fundamentals, last_price)
    if pb_estimate:
        estimates['Price-to-Book'] = pb_estimate
    
    # Return average and breakdown
    if estimates:
        fair_price = float(np.mean(list(estimates.values())))
        return {
            'fair_price': fair_price,
            'current_price': last_price,
            'upside': ((fair_price - last_price) / last_price) * 100,
            'methods': estimates
        }
    
    return {
        'fair_price': last_price,
        'current_price': last_price,
        'upside': 0,
        'methods': {}
    }


def _pe_valuation(fundamentals: dict, current_price: float) -> float:
    """P/E based valuation using market average or peer data."""
    pe = fundamentals.get('trailingPE') or fundamentals.get('forwardPE')
    if pe and pe > 0 and pe < 100:  # Sanity check
        # Simple: assume intrinsic = earnings * market_avg_pe
        # For now, use current P/E as proxy
        return current_price
    return None


def _gordon_growth_valuation(fundamentals: dict, current_price: float) -> float:
    """
    Gordon Growth Model: P = D1 / (r - g)
    where D1 = next dividend, r = discount rate, g = growth rate
    """
    div_yield = fundamentals.get('dividendYield')
    if div_yield and div_yield > 0:
        # Assumptions
        r = 0.08  # 8% discount rate
        g = 0.025  # 2.5% growth rate
        d1 = current_price * div_yield * (1 + g)
        if r > g:
            return d1 / (r - g)
    return None


def _price_to_book_valuation(fundamentals: dict, current_price: float) -> float:
    """P/B valuation: if we know the ratio, estimate fair price."""
    pb = fundamentals.get('priceToBook')
    if pb and pb > 0 and pb < 20:
        # Assume sector average P/B is around 3-5 (simplification)
        sector_avg_pb = 3.5
        adjustment = sector_avg_pb / pb if pb > 0 else 1.0
        return current_price * adjustment
    return None


def _simple_dcf_valuation(ticker: str, current_price: float) -> float:
    """
    Simple DCF using historical free cash flow or earnings.
    Forecast 5 years of cash flows, discount to present.
    """
    try:
        t = yf.Ticker(ticker)
        info = t.info if hasattr(t, 'info') else {}
        
        # Get trailing twelve months free cash flow
        fcf = info.get('freeCashflow')
        if not fcf or fcf <= 0:
            return None
        
        # Simple forecast: assume 5% annual growth
        growth_rate = 0.05
        discount_rate = 0.10
        terminal_growth = 0.025
        
        pv_fcf = 0
        forecast_fcf = fcf
        for year in range(1, 6):
            forecast_fcf *= (1 + growth_rate)
            pv_fcf += forecast_fcf / ((1 + discount_rate) ** year)
        
        # Terminal value
        terminal_fcf = forecast_fcf * (1 + terminal_growth)
        terminal_value = terminal_fcf / (discount_rate - terminal_growth)
        pv_terminal = terminal_value / ((1 + discount_rate) ** 5)
        
        # Enterprise value
        enterprise_value = pv_fcf + pv_terminal
        
        # Simple: assume equity value ~ enterprise value (ignore net debt)
        shares_outstanding = info.get('sharesOutstanding', 1)
        if shares_outstanding and shares_outstanding > 0:
            dcf_price = enterprise_value / shares_outstanding
            return dcf_price if dcf_price > 0 else None
    
    except Exception as e:
        pass
    
    return None

