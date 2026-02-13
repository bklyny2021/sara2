#!/usr/bin/env python3
"""
Trading Bot Market Research Module
Real-time stock analysis and pattern detection system
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class StockResearch:
    def __init__(self):
        self.watchlist = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
        self.data_cache = {}
        self.patterns_found = []
        
    def fetch_market_data(self, symbol, period='6mo'):
        """Fetch comprehensive stock data"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            # Add basic technical indicators
            data['RSI'] = self.calculate_rsi(data['Close'])
            data['MA_20'] = data['Close'].rolling(20).mean()
            data['MA_50'] = data['Close'].rolling(50).mean()
            data['Volume_MA'] = data['Volume'].rolling(20).mean()
            
            self.data_cache[symbol] = data
            print(f"✅ {symbol}: {len(data)} days loaded | Price: ${data['Close'][-1]:.2f}")
            return data
            
        except Exception as e:
            print(f"❌ Error loading {symbol}: {e}")
            return None
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI technical indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze_patterns(self, symbol):
        """Identify trading patterns and opportunities"""
        if symbol not in self.data_cache:
            self.fetch_market_data(symbol)
        
        data = self.data_cache[symbol]
        analysis = {}
        
        # Current trend analysis
        current_price = data['Close'][-1]
        ma_20 = data['MA_20'][-1]
        ma_50 = data['MA_50'][-1]
        rsi = data['RSI'][-1]
        
        # Trend determination
        if current_price > ma_20 > ma_50:
            analysis['trend'] = 'BULLISH'
            analysis['strength'] = 'STRONG' if rsi > 50 and rsi < 70 else 'WEAK'
        elif current_price < ma_20 < ma_50:
            analysis['trend'] = 'BEARISH'
            analysis['strength'] = 'STRONG' if rsi < 50 and rsi > 30 else 'WEAK'
        else:
            analysis['trend'] = 'SIDEWAYS'
            analysis['strength'] = 'UNCLEAR'
        
        # Volume analysis
        current_volume = data['Volume'][-1]
        volume_ma = data['Volume_MA'][-1]
        volume_signal = current_volume > volume_ma * 1.5
        analysis['volume_anomaly'] = 'HIGH' if volume_signal else 'NORMAL'
        
        # RSI signals
        if rsi > 70:
            analysis['rsi_signal'] = 'OVERBOUGHT'
        elif rsi < 30:
            analysis['rsi_signal'] = 'OVERSOLD'
        else:
            analysis['rsi_signal'] = 'NEUTRAL'
        
        # Price action patterns (simplified)
        analysis['support'] = self.find_support_level(data)
        analysis['resistance'] = self.find_resistance_level(data)
        
        # Recent performance
        week_change = ((current_price - data['Close'][-5]) / data['Close'][-5]) * 100
        analysis['week_change'] = f"{week_change:+.2f}%"
        
        return analysis
    
    def find_support_level(self, data, lookback=20):
        """Find recent support level"""
        recent_lows = data['Low'].tail(lookback)
        return recent_lows.min()
    
    def find_resistance_level(self, data, lookback=20):
        """Find recent resistance level"""
        recent_highs = data['High'].tail(lookback)
        return recent_highs.max()
    
    def generate_trading_signals(self, symbol):
        """Generate buy/sell/hold signals"""
        analysis = self.analyze_patterns(symbol)
        signal = 'HOLD'
        confidence = 50
        
        # Simple signal logic (will be refined as we learn)
        trend = analysis.get('trend', '')
        rsi = analysis.get('rsi_signal', '')
        volume = analysis.get('volume_anomaly', '')
        
        if trend == 'BULLISH' and rsi != 'OVERBOUGHT' and volume == 'HIGH':
            signal = 'BUY'
            confidence = 75
        elif trend == 'BEARISH' and rsi != 'OVERSOLD' and volume == 'HIGH':
            signal = 'SELL'
            confidence = 75
        elif trend == 'SIDEWAYS':
            signal = 'WAIT'
            confidence = 60
        
        return {
            'signal': signal,
            'confidence': confidence,
            'reasoning': f"Trend: {trend}, RSI: {rsi}, Volume: {volume}"
        }
    
    def get_market_overview(self):
        """Overall market analysis"""
        print("📊 MARKET RESEARCH DASHBOARD")
        print("=" * 50)
        
        overall_sentiment = {'buy': 0, 'sell': 0, 'hold': 0}
        
        for symbol in self.watchlist:
            analysis = self.analyze_patterns(symbol)
            signal = self.generate_trading_signals(symbol)
            
            print(f"\n{symbol}:")
            print(f"  Price: ${self.data_cache[symbol]['Close'][-1]:.2f}")
            print(f"  Trend: {analysis['trend']} ({analysis['strength']})")
            print(f"  RSI: {analysis['rsi_signal']} ({self.data_cache[symbol]['RSI'][-1]:.1f})")
            print(f"  Signal: {signal['signal']} (Confidence: {signal['confidence']}%)")
            print(f"  Week Change: {analysis['week_change']}")
            
            # Count signals for overall sentiment
            overall_sentiment[signal['signal'].lower()] += 1
        
        # Determine overall market direction
        if overall_sentiment['buy'] > overall_sentiment['sell']:
            market_trend = 'BULLISH'
        elif overall_sentiment['sell'] > overall_sentiment['buy']:
            market_trend = 'BEARISH'
        else:
            market_trend = 'MIXED'
        
        print(f"\n🎯 OVERALL MARKET: {market_trend}")
        return overall_sentiment, market_trend

def main():
    """Run market research analysis"""
    researcher = StockResearch()
    
    # Load data for all stocks
    print("Loading market data...")
    for symbol in researcher.watchlist:
        researcher.fetch_market_data(symbol)
    
    # Generate comprehensive analysis
    sentiment, trend = researcher.get_market_overview()
    
    # Detailed pattern tracking
    print(f"\n📈 PATTERN ANALYSIS COMPLETE")
    print(f"Market Sentiment: {sentiment}")
    print(f"Next analysis in 30 minutes...")
    
    return researcher

if __name__ == "__main__":
    researcher = main()