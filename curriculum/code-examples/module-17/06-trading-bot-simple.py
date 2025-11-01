"""
Module 17.5 & 17.8: Simple AI Trading Bot
A beginner-friendly implementation showing core trading bot patterns

This bot demonstrates:
- Price monitoring
- Technical indicator calculation
- AI-powered decision making
- Paper trading simulation
- Risk management basics

⚠️  This is a LEARNING example - start with paper trading only!
"""

import requests
import time
from datetime import datetime


class SimpleTradingBot:
    """
    A simple AI trading bot for learning purposes
    
    This bot:
    1. Fetches current price
    2. Calculates basic indicators (RSI)
    3. Asks AI for trading advice
    4. Simulates trades (paper trading)
    """
    
    def __init__(self, llm_client, initial_capital: float = 10000):
        self.llm = llm_client
        self.portfolio = {
            'USD': initial_capital,
            'BTC': 0
        }
        self.trade_history = []
        
        # Risk management
        self.max_position_size_percent = 0.10  # Max 10% per trade
        self.stop_loss_percent = 0.05          # 5% stop loss
    
    def get_price(self, symbol: str) -> float:
        """Fetch current price from CoinGecko API"""
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": symbol.lower(),
            "vs_currencies": "usd"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data[symbol.lower()]["usd"]
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None
    
    def calculate_rsi(self, prices: list, period: int = 14) -> float:
        """
        Calculate Relative Strength Index
        
        Note: This is a simplified version for teaching.
        For production, use ta-lib or pandas-ta.
        """
        if len(prices) < period + 1:
            return 50  # Neutral if not enough data
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    async def analyze_market(self, symbol: str) -> dict:
        """Use AI to analyze market and suggest action"""
        
        # Gather market data
        price = self.get_price(symbol)
        if not price:
            return {'error': 'Could not fetch price'}
        
        # Calculate indicators (in production, fetch historical data)
        rsi = 45  # Placeholder - would calculate from historical data
        
        # Build prompt for AI
        prompt = f"""
        You are a cryptocurrency trading advisor. Analyze the following data:
        
        Asset: {symbol}
        Current Price: ${price:,.2f}
        RSI (14): {rsi}
        Portfolio: ${self.portfolio['USD']:.2f} USD, {self.portfolio.get(symbol, 0):.6f} {symbol}
        
        Based on this data, provide:
        ACTION: [BUY/SELL/HOLD]
        REASONING: [Your analysis in 1-2 sentences]
        CONFIDENCE: [1-10]
        POSITION_SIZE: [Percentage of available capital, 0-10%]
        
        Consider RSI levels:
        - RSI < 30: Oversold (potential buy)
        - RSI > 70: Overbought (potential sell)
        - RSI 30-70: Neutral
        """
        
        # Get AI analysis
        response = await self.llm.chat(prompt)
        
        # Parse response (simple parsing for demo)
        parsed = self._parse_ai_response(response)
        parsed['price'] = price
        
        return parsed
    
    def _parse_ai_response(self, response: str) -> dict:
        """Parse AI response into structured data"""
        lines = response.split('\n')
        result = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                result[key] = value
        
        return result
    
    def execute_trade(self, symbol: str, action: str, amount: float, price: float):
        """
        Simulate trade execution (paper trading)
        
        Args:
            symbol: Asset symbol
            action: 'BUY' or 'SELL'
            amount: Amount to trade
            price: Current price
        """
        if action == "BUY":
            cost = amount * price
            
            if self.portfolio["USD"] >= cost:
                self.portfolio["USD"] -= cost
                self.portfolio[symbol] = self.portfolio.get(symbol, 0) + amount
                
                self.trade_history.append({
                    "action": "BUY",
                    "symbol": symbol,
                    "amount": amount,
                    "price": price,
                    "cost": cost,
                    "timestamp": datetime.now()
                })
                
                print(f"✅ BUY: {amount:.6f} {symbol} at ${price:,.2f}")
            else:
                print(f"❌ Insufficient funds. Need ${cost:.2f}, have ${self.portfolio['USD']:.2f}")
        
        elif action == "SELL":
            if self.portfolio.get(symbol, 0) >= amount:
                revenue = amount * price
                
                self.portfolio[symbol] -= amount
                self.portfolio["USD"] += revenue
                
                self.trade_history.append({
                    "action": "SELL",
                    "symbol": symbol,
                    "amount": amount,
                    "price": price,
                    "revenue": revenue,
                    "timestamp": datetime.now()
                })
                
                print(f"✅ SELL: {amount:.6f} {symbol} at ${price:,.2f}")
            else:
                print(f"❌ Insufficient {symbol}. Need {amount:.6f}, have {self.portfolio.get(symbol, 0):.6f}")
    
    def calculate_position_size(self, action: str, price: float) -> float:
        """
        Calculate safe position size based on risk management rules
        
        Returns amount of asset to trade
        """
        if action == "BUY":
            # Use 10% of available USD
            risk_amount = self.portfolio["USD"] * self.max_position_size_percent
            amount = risk_amount / price
            return amount
        
        elif action == "SELL":
            # Sell 50% of holdings
            return self.portfolio.get("BTC", 0) * 0.5
        
        return 0
    
    async def run(self, symbol: str):
        """Main bot execution loop (single iteration)"""
        
        print(f"\n{'='*60}")
        print(f"🤖 AI Trading Bot - {symbol}")
        print(f"{'='*60}")
        
        # Analyze market
        analysis = await self.analyze_market(symbol)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return
        
        # Display AI analysis
        print(f"\n📊 AI Analysis:")
        print(f"   Action: {analysis.get('action', 'UNKNOWN')}")
        print(f"   Reasoning: {analysis.get('reasoning', 'N/A')}")
        print(f"   Confidence: {analysis.get('confidence', 'N/A')}/10")
        
        # Execute trade if confidence is high enough
        action = analysis.get('action', '').upper()
        confidence = int(analysis.get('confidence', 0))
        
        if confidence >= 7 and action in ['BUY', 'SELL']:
            amount = self.calculate_position_size(action, analysis['price'])
            self.execute_trade(symbol, action, amount, analysis['price'])
        else:
            print(f"⏸️  No action taken (confidence too low or HOLD signal)")
        
        # Display portfolio
        print(f"\n💼 Portfolio:")
        print(f"   USD: ${self.portfolio['USD']:,.2f}")
        print(f"   {symbol}: {self.portfolio.get(symbol, 0):.6f}")
        
        total_value = self.portfolio['USD'] + (self.portfolio.get(symbol, 0) * analysis['price'])
        print(f"   Total Value: ${total_value:,.2f}")
        
        print(f"\n{'='*60}\n")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example usage of the trading bot"""
    
    # You would initialize your LLM client here
    # from llm_agnostic_framework import load_agent_from_config
    # llm = load_agent_from_config()
    
    # For demo, using a mock LLM
    class MockLLM:
        async def chat(self, prompt):
            return """
            ACTION: HOLD
            REASONING: Market is sideways, RSI neutral. Wait for clearer signal.
            CONFIDENCE: 6
            POSITION_SIZE: 0%
            """
    
    llm = MockLLM()
    
    # Create and run bot
    bot = SimpleTradingBot(llm_client=llm, initial_capital=10000)
    
    # Run analysis (in production, this would be in a loop)
    await bot.run("bitcoin")
    
    # Show trade history
    if bot.trade_history:
        print("📜 Trade History:")
        for trade in bot.trade_history:
            print(f"   {trade}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

