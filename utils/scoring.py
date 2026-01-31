"""
Comprehensive scoring system for stock analysis
Combines technical, fundamental, forecast, and sentiment signals
"""

import numpy as np
import pandas as pd


def calculate_technical_score(indicators_df):
    """
    Calculate technical analysis score (0-10)
    
    Components:
    - RSI (0.30 weight): 50% score
    - Price vs SMA50 (0.25 weight)
    - Price vs SMA200 (0.25 weight)
    - MACD (0.15 weight)
    - Bollinger Bands (0.05 weight)
    """
    try:
        if indicators_df is None or indicators_df.empty:
            return {'score': 5.0, 'reasoning': 'Insufficient data', 'components': {}}
        
        components = {}
        
        # RSI Score (30/70 levels)
        if 'RSI' in indicators_df.columns:
            rsi = float(indicators_df['RSI'].iloc[-1])
            if rsi < 30:
                rsi_score = 8.0  # Oversold, bullish
                rsi_reason = "Oversold (RSI < 30)"
            elif rsi > 70:
                rsi_score = 2.0  # Overbought, bearish
                rsi_reason = "Overbought (RSI > 70)"
            elif rsi < 50:
                rsi_score = 6.0  # Neutral-bullish
                rsi_reason = f"Neutral-Bullish (RSI {rsi:.1f})"
            else:
                rsi_score = 5.0  # Neutral
                rsi_reason = f"Neutral (RSI {rsi:.1f})"
            
            components['RSI'] = {'score': rsi_score, 'reason': rsi_reason}
        else:
            components['RSI'] = {'score': 5.0, 'reason': 'RSI not available'}
        
        # Price vs SMA50
        if 'SMA_50' in indicators_df.columns and 'Close' in indicators_df.columns:
            current_price = float(indicators_df['Close'].iloc[-1])
            sma50 = float(indicators_df['SMA_50'].iloc[-1])
            
            if sma50 > 0:
                pct_above_sma50 = ((current_price - sma50) / sma50) * 100
                if pct_above_sma50 > 5:
                    sma50_score = 7.0
                    sma50_reason = f"Above SMA50 by {pct_above_sma50:.1f}%"
                elif pct_above_sma50 < -5:
                    sma50_score = 3.0
                    sma50_reason = f"Below SMA50 by {abs(pct_above_sma50):.1f}%"
                else:
                    sma50_score = 5.0
                    sma50_reason = f"Near SMA50 ({pct_above_sma50:+.1f}%)"
                
                components['SMA50'] = {'score': sma50_score, 'reason': sma50_reason}
            else:
                components['SMA50'] = {'score': 5.0, 'reason': 'SMA50 calculation error'}
        else:
            components['SMA50'] = {'score': 5.0, 'reason': 'SMA50 not available'}
        
        # Price vs SMA200
        if 'SMA_200' in indicators_df.columns and 'Close' in indicators_df.columns:
            current_price = float(indicators_df['Close'].iloc[-1])
            sma200 = float(indicators_df['SMA_200'].iloc[-1])
            
            if sma200 > 0:
                pct_above_sma200 = ((current_price - sma200) / sma200) * 100
                if pct_above_sma200 > 10:
                    sma200_score = 7.5
                    sma200_reason = f"Above SMA200 by {pct_above_sma200:.1f}%"
                elif pct_above_sma200 < -10:
                    sma200_score = 2.5
                    sma200_reason = f"Below SMA200 by {abs(pct_above_sma200):.1f}%"
                else:
                    sma200_score = 5.0
                    sma200_reason = f"Near SMA200 ({pct_above_sma200:+.1f}%)"
                
                components['SMA200'] = {'score': sma200_score, 'reason': sma200_reason}
            else:
                components['SMA200'] = {'score': 5.0, 'reason': 'SMA200 calculation error'}
        else:
            components['SMA200'] = {'score': 5.0, 'reason': 'SMA200 not available'}
        
        # MACD
        if 'MACD' in indicators_df.columns and 'MACD_Signal' in indicators_df.columns:
            macd = float(indicators_df['MACD'].iloc[-1])
            macd_signal = float(indicators_df['MACD_Signal'].iloc[-1])
            
            if macd > macd_signal:
                macd_score = 6.5
                macd_reason = "MACD above signal (bullish)"
            else:
                macd_score = 3.5
                macd_reason = "MACD below signal (bearish)"
            
            components['MACD'] = {'score': macd_score, 'reason': macd_reason}
        else:
            components['MACD'] = {'score': 5.0, 'reason': 'MACD not available'}
        
        # Bollinger Bands
        if 'BB_High' in indicators_df.columns and 'BB_Low' in indicators_df.columns:
            try:
                current_price = float(indicators_df['Close'].iloc[-1])
                bb_high = float(indicators_df['BB_High'].iloc[-1])
                bb_low = float(indicators_df['BB_Low'].iloc[-1])
                
                if bb_high > bb_low:
                    bb_position = (current_price - bb_low) / (bb_high - bb_low)
                    if bb_position > 0.8:
                        bb_score = 3.0
                        bb_reason = "Near upper band (potential pullback)"
                    elif bb_position < 0.2:
                        bb_score = 7.0
                        bb_reason = "Near lower band (potential bounce)"
                    else:
                        bb_score = 5.0
                        bb_reason = "Within normal range"
                else:
                    bb_score = 5.0
                    bb_reason = "BB calculation error"
                
                components['Bollinger'] = {'score': bb_score, 'reason': bb_reason}
            except:
                components['Bollinger'] = {'score': 5.0, 'reason': 'BB calculation error'}
        else:
            components['Bollinger'] = {'score': 5.0, 'reason': 'Bollinger Bands not available'}
        
        # Calculate weighted score
        weights = {
            'RSI': 0.30,
            'SMA50': 0.25,
            'SMA200': 0.25,
            'MACD': 0.15,
            'Bollinger': 0.05
        }
        
        total_score = 0
        for component_name, weight in weights.items():
            if component_name in components:
                total_score += components[component_name]['score'] * weight
        
        reasoning = "Technical indicators show "
        if total_score >= 7:
            reasoning += "strong bullish signals"
        elif total_score >= 6:
            reasoning += "bullish signals"
        elif total_score >= 4:
            reasoning += "mixed signals"
        elif total_score >= 3:
            reasoning += "bearish signals"
        else:
            reasoning += "strong bearish signals"
        
        return {
            'score': total_score,
            'reasoning': reasoning,
            'components': components
        }
    
    except Exception as e:
        return {
            'score': 5.0,
            'reasoning': f'Technical analysis error: {str(e)}',
            'components': {}
        }


def calculate_fundamental_score(fundamentals):
    """
    Calculate fundamental score (0-10)
    
    Components:
    - P/E Ratio (0.35 weight)
    - Beta (0.25 weight)
    - Dividend Yield (0.20 weight)
    - Market Cap/Size (0.20 weight)
    """
    try:
        if not fundamentals:
            return {'score': 5.0, 'reasoning': 'No fundamental data available', 'components': {}}
        
        components = {}
        
        # P/E Ratio (lower is better, but context matters)
        if 'trailingPE' in fundamentals and fundamentals['trailingPE']:
            pe = float(fundamentals['trailingPE'])
            if pe < 15:
                pe_score = 8.0
                pe_reason = f"Low P/E ({pe:.1f}) - Undervalued"
            elif pe < 20:
                pe_score = 7.0
                pe_reason = f"Fair P/E ({pe:.1f})"
            elif pe < 30:
                pe_score = 5.0
                pe_reason = f"Moderate P/E ({pe:.1f})"
            else:
                pe_score = 3.0
                pe_reason = f"High P/E ({pe:.1f}) - Expensive"
            
            components['P/E'] = {'score': pe_score, 'reason': pe_reason}
        else:
            components['P/E'] = {'score': 5.0, 'reason': 'P/E not available'}
        
        # Beta (lower volatility preferred)
        if 'beta' in fundamentals and fundamentals['beta']:
            beta = float(fundamentals['beta'])
            if beta < 0.8:
                beta_score = 8.0
                beta_reason = f"Low Beta ({beta:.2f}) - Low volatility"
            elif beta < 1.2:
                beta_score = 7.0
                beta_reason = f"Moderate Beta ({beta:.2f})"
            elif beta < 1.5:
                beta_score = 5.0
                beta_reason = f"Elevated Beta ({beta:.2f})"
            else:
                beta_score = 3.0
                beta_reason = f"High Beta ({beta:.2f}) - High volatility"
            
            components['Beta'] = {'score': beta_score, 'reason': beta_reason}
        else:
            components['Beta'] = {'score': 5.0, 'reason': 'Beta not available'}
        
        # Dividend Yield
        if 'dividendYield' in fundamentals and fundamentals['dividendYield']:
            div_yield = float(fundamentals['dividendYield']) * 100
            if div_yield > 4:
                div_score = 8.0
                div_reason = f"High dividend ({div_yield:.2f}%)"
            elif div_yield > 2:
                div_score = 7.0
                div_reason = f"Good dividend ({div_yield:.2f}%)"
            elif div_yield > 0:
                div_score = 5.0
                div_reason = f"Modest dividend ({div_yield:.2f}%)"
            else:
                div_score = 4.0
                div_reason = "No dividend"
            
            components['Dividend'] = {'score': div_score, 'reason': div_reason}
        else:
            components['Dividend'] = {'score': 4.0, 'reason': 'Dividend data not available'}
        
        # Market Cap (size matters for stability)
        if 'marketCap' in fundamentals and fundamentals['marketCap']:
            market_cap = float(fundamentals['marketCap'])
            if market_cap > 1e11:  # Over $100B
                cap_score = 8.0
                cap_reason = "Large cap (>$100B) - More stable"
            elif market_cap > 1e10:  # Over $10B
                cap_score = 7.0
                cap_reason = "Mid cap ($10B-$100B)"
            elif market_cap > 1e9:  # Over $1B
                cap_score = 5.0
                cap_reason = "Small cap ($1B-$10B)"
            else:
                cap_score = 3.0
                cap_reason = "Micro cap (<$1B) - Risky"
            
            components['Market Cap'] = {'score': cap_score, 'reason': cap_reason}
        else:
            components['Market Cap'] = {'score': 5.0, 'reason': 'Market cap not available'}
        
        # Calculate weighted score
        weights = {
            'P/E': 0.35,
            'Beta': 0.25,
            'Dividend': 0.20,
            'Market Cap': 0.20
        }
        
        total_score = 0
        for component_name, weight in weights.items():
            if component_name in components:
                total_score += components[component_name]['score'] * weight
        
        reasoning = "Fundamentals look "
        if total_score >= 7:
            reasoning += "strong"
        elif total_score >= 5:
            reasoning += "reasonable"
        else:
            reasoning += "weak"
        
        return {
            'score': total_score,
            'reasoning': reasoning,
            'components': components
        }
    
    except Exception as e:
        return {
            'score': 5.0,
            'reasoning': f'Fundamental analysis error: {str(e)}',
            'components': {}
        }


def calculate_forecast_score(backtest_metrics):
    """
    Calculate forecast confidence score (0-10)
    
    Components:
    - Direction Accuracy (0.50 weight)
    - Prediction Accuracy/MAE (0.35 weight)
    - Sample Size (0.15 weight)
    """
    try:
        if not backtest_metrics:
            return {
                'score': 5.0,
                'confidence': 'MEDIUM',
                'reasoning': 'Forecast model not available',
                'components': {}
            }
        
        components = {}
        
        # Direction Accuracy
        if 'direction_accuracy' in backtest_metrics:
            acc = float(backtest_metrics['direction_accuracy'])
            if acc > 0.65:
                acc_score = 8.0
                acc_reason = f"High accuracy ({acc*100:.0f}%)"
            elif acc > 0.55:
                acc_score = 6.0
                acc_reason = f"Good accuracy ({acc*100:.0f}%)"
            elif acc > 0.50:
                acc_score = 4.0
                acc_reason = f"Slight edge ({acc*100:.0f}%)"
            else:
                acc_score = 2.0
                acc_reason = f"Below random ({acc*100:.0f}%)"
            
            components['Direction Accuracy'] = {'score': acc_score, 'reason': acc_reason}
        else:
            components['Direction Accuracy'] = {'score': 4.0, 'reason': 'Accuracy not available'}
        
        # MAE (Mean Absolute Error) - lower is better
        if 'mae' in backtest_metrics and 'rmse' in backtest_metrics:
            try:
                mae = float(backtest_metrics['mae'])
                rmse = float(backtest_metrics['rmse'])
                
                # MAE as percentage of recent prices (estimate)
                if rmse > 0:
                    mae_pct = (mae / rmse) * 100 if rmse > 0 else 100
                    
                    if mae_pct < 2:
                        mae_score = 8.0
                        mae_reason = f"Very accurate predictions"
                    elif mae_pct < 5:
                        mae_score = 6.5
                        mae_reason = f"Good prediction accuracy"
                    elif mae_pct < 10:
                        mae_score = 5.0
                        mae_reason = f"Moderate prediction accuracy"
                    else:
                        mae_score = 3.0
                        mae_reason = f"Lower accuracy"
                    
                    components['Prediction Accuracy'] = {'score': mae_score, 'reason': mae_reason}
                else:
                    components['Prediction Accuracy'] = {'score': 5.0, 'reason': 'Accuracy calculation error'}
            except:
                components['Prediction Accuracy'] = {'score': 5.0, 'reason': 'Prediction data not available'}
        else:
            components['Prediction Accuracy'] = {'score': 5.0, 'reason': 'Prediction metrics not available'}
        
        # Sample Size (more test periods = more reliable)
        if 'test_periods' in backtest_metrics:
            test_periods = int(backtest_metrics['test_periods'])
            if test_periods > 50:
                sample_score = 8.0
                sample_reason = f"Large sample ({test_periods} periods)"
            elif test_periods > 20:
                sample_score = 7.0
                sample_reason = f"Good sample ({test_periods} periods)"
            elif test_periods > 10:
                sample_score = 5.0
                sample_reason = f"Small sample ({test_periods} periods)"
            else:
                sample_score = 3.0
                sample_reason = f"Very small sample ({test_periods} periods)"
            
            components['Sample Size'] = {'score': sample_score, 'reason': sample_reason}
        else:
            components['Sample Size'] = {'score': 5.0, 'reason': 'Sample info not available'}
        
        # Calculate weighted score
        weights = {
            'Direction Accuracy': 0.50,
            'Prediction Accuracy': 0.35,
            'Sample Size': 0.15
        }
        
        total_score = 0
        for component_name, weight in weights.items():
            if component_name in components:
                total_score += components[component_name]['score'] * weight
        
        # Determine confidence level
        if total_score >= 7:
            confidence = 'HIGH'
        elif total_score >= 5:
            confidence = 'MEDIUM'
        else:
            confidence = 'LOW'
        
        reasoning = f"Model confidence is {confidence.lower()} based on backtest performance"
        
        return {
            'score': total_score,
            'confidence': confidence,
            'reasoning': reasoning,
            'components': components
        }
    
    except Exception as e:
        return {
            'score': 5.0,
            'confidence': 'MEDIUM',
            'reasoning': f'Forecast analysis error: {str(e)}',
            'components': {}
        }


def calculate_sentiment_score(sentiment_data):
    """
    Calculate sentiment score (0-10)
    
    Components:
    - Overall sentiment (0.50 weight)
    - News flow/Articles (0.25 weight)
    - Recent trend (0.25 weight)
    """
    try:
        if not sentiment_data:
            return {
                'score': 5.0,
                'sentiment': 'NEUTRAL',
                'reasoning': 'No sentiment data available',
                'components': {},
                'articles': []
            }
        
        components = {}
        
        # Overall sentiment
        daily_sentiment = sentiment_data.get('daily_sentiment', 0)
        if isinstance(daily_sentiment, (list, np.ndarray)):
            daily_sentiment = float(daily_sentiment[0]) if len(daily_sentiment) > 0 else 0
        else:
            daily_sentiment = float(daily_sentiment)
        
        if daily_sentiment > 0.3:
            sent_score = 8.0
            sent_reason = "Strong positive sentiment"
            sentiment_label = 'POSITIVE'
        elif daily_sentiment > 0.1:
            sent_score = 6.5
            sent_reason = "Positive sentiment"
            sentiment_label = 'POSITIVE'
        elif daily_sentiment > -0.1:
            sent_score = 5.0
            sent_reason = "Neutral sentiment"
            sentiment_label = 'NEUTRAL'
        elif daily_sentiment > -0.3:
            sent_score = 3.5
            sent_reason = "Negative sentiment"
            sentiment_label = 'NEGATIVE'
        else:
            sent_score = 2.0
            sent_reason = "Strong negative sentiment"
            sentiment_label = 'NEGATIVE'
        
        components['Overall'] = {'score': sent_score, 'reason': sent_reason}
        
        # News flow
        recent_articles = sentiment_data.get('recent_articles', [])
        article_count = len(recent_articles) if recent_articles else 0
        
        if article_count > 5:
            article_score = 6.0
            article_reason = f"High news flow ({article_count} recent articles)"
        elif article_count > 2:
            article_score = 5.0
            article_reason = f"Normal news flow ({article_count} articles)"
        elif article_count > 0:
            article_score = 4.0
            article_reason = f"Low news flow ({article_count} articles)"
        else:
            article_score = 3.0
            article_reason = "No recent news"
        
        components['Articles'] = {'score': article_score, 'reason': article_reason}
        
        # Trend (based on sentiment history)
        trend_score = 5.0
        trend_reason = "Neutral trend"
        components['Trend'] = {'score': trend_score, 'reason': trend_reason}
        
        # Calculate weighted score
        weights = {
            'Overall': 0.50,
            'Articles': 0.25,
            'Trend': 0.25
        }
        
        total_score = 0
        for component_name, weight in weights.items():
            if component_name in components:
                total_score += components[component_name]['score'] * weight
        
        reasoning = f"Sentiment is {sentiment_label.lower()}"
        
        return {
            'score': total_score,
            'sentiment': sentiment_label,
            'reasoning': reasoning,
            'components': components,
            'articles': recent_articles
        }
    
    except Exception as e:
        return {
            'score': 5.0,
            'sentiment': 'NEUTRAL',
            'reasoning': f'Sentiment analysis error: {str(e)}',
            'components': {},
            'articles': []
        }


def generate_complete_score(ticker, indicators_df, current_price, fundamentals, 
                          backtest_metrics, sentiment_data):
    """
    Generate comprehensive score combining all factors
    
    Returns:
        Dict with overall score, component scores, and recommendation
    """
    try:
        # Calculate component scores
        technical = calculate_technical_score(indicators_df)
        fundamental = calculate_fundamental_score(fundamentals)
        forecast = calculate_forecast_score(backtest_metrics)
        sentiment = calculate_sentiment_score(sentiment_data)
        
        # Weighted overall score
        overall_score = (
            technical['score'] * 0.30 +
            fundamental['score'] * 0.25 +
            forecast['score'] * 0.25 +
            sentiment['score'] * 0.20
        )
        
        # Generate recommendation
        if overall_score >= 7.5:
            recommendation = 'STRONG BUY'
            emoji = '🟢🟢'
            description = 'Excellent buying opportunity with strong signals across all metrics'
        elif overall_score >= 6.5:
            recommendation = 'BUY'
            emoji = '🟢'
            description = 'Good buying opportunity with mostly positive signals'
        elif overall_score >= 5.5:
            recommendation = 'HOLD'
            emoji = '⚪'
            description = 'Mixed signals suggest waiting for clearer direction'
        elif overall_score >= 4.5:
            recommendation = 'SELL'
            emoji = '🔴'
            description = 'Negative signals suggest looking for exits'
        else:
            recommendation = 'STRONG SELL'
            emoji = '🔴🔴'
            description = 'Strong negative signals, avoid or exit position'
        
        # Risk assessment
        if overall_score > 7:
            risk_level = 'LOW'
        elif overall_score > 5:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'HIGH'
        
        # Confidence level
        confidence = forecast.get('confidence', 'MEDIUM')
        
        return {
            'ticker': ticker,
            'price': current_price,
            'overall_score': overall_score,
            'summary': {
                'recommendation': recommendation,
                'emoji': emoji,
                'description': description,
                'score': overall_score,
                'risk_level': risk_level,
                'confidence': confidence
            },
            'technical': technical,
            'fundamental': fundamental,
            'forecast': forecast,
            'sentiment': sentiment
        }
    
    except Exception as e:
        print(f"Error in generate_complete_score: {e}")
        return None
