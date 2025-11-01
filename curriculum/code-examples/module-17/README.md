# Module 17: AI Agent Application Development - Code Examples

This directory contains complete, production-ready code examples for Module 17 of the cryptocurrency curriculum. These examples support the teaching material and provide students with working implementations they can study, modify, and extend.

## 📁 File Structure

### Core Framework

**`05-llm-agnostic-framework.py`** - LLM-Agnostic Agent Framework (Module 17.10)
- Abstract base agent class
- OpenAI, Anthropic, and Ollama provider implementations
- Unified tool calling system
- Cost tracking and conversation management
- Configuration-driven provider switching

**Supporting Curriculum Sections:** 17.10 LLM-Agnostic Framework Implementation

---

### Data Gathering & Analysis

**`01-data-gathering-pipeline.py`** - Multi-Source Data Gathering (Module 17.3)
- Parallel data fetching from multiple sources
- Market data aggregation
- Error handling and data validation
- Unified data format

**Supporting Curriculum Sections:** 17.3 Data Gathering & Information Synthesis

---

**`02-social-sentiment-analysis.py`** - Social Media Sentiment Analysis (Module 17.4)
- X (Twitter) API integration
- Reddit API integration
- Discord and Telegram monitoring
- Sentiment analysis with FinBERT and LLMs
- Sentiment aggregation and weighting
- Trending topic detection
- Influencer tracking

**Supporting Curriculum Sections:** 17.4 Social Media Sentiment Analysis

---

### Decision Making

**`03-multi-source-decision-engine.py`** - Multi-Source Decision Engine (Module 17.6)
- Technical analysis integration
- Social sentiment weighting
- On-chain metrics analysis
- Market fundamentals evaluation
- News analysis
- Weighted scoring system
- LLM synthesis for final decisions

**Supporting Curriculum Sections:** 17.6 Multi-Source Decision Making

---

### Blockchain Integration

**`04-blockchain-defi-integration.py`** - Blockchain & DeFi Integration (Module 17.7)
- Web3 connection setup
- Whale wallet monitoring
- DEX price monitoring (Uniswap V3)
- DEX trading execution
- Gas price optimization
- ERC-20 event tracking

**Supporting Curriculum Sections:** 17.7 Blockchain & DeFi Integration

⚠️  **SECURITY WARNING:** Never commit private keys to version control. Use environment variables.

---

### Trading Bot

**`06-trading-bot-simple.py`** - Simple AI Trading Bot (Module 17.5, 17.8, 17.9)
- Price monitoring from CoinGecko API
- Basic RSI calculation
- AI-powered market analysis
- Paper trading simulation
- Risk management (position sizing, stop-loss)
- Trade history tracking

**Supporting Curriculum Sections:** 
- 17.5 Building Your First AI Trading Bot
- 17.8 Trading Bot Fundamentals
- 17.9 Student Customization Guide

⚠️  **TRADING WARNING:** Start with paper trading only. Never risk real money without thorough testing.

---

## 🚀 Getting Started

### Prerequisites

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install web3 requests tweepy praw discord.py anthropic openai httpx
pip install transformers torch  # For sentiment analysis
pip install pyyaml  # For configuration
```

### Configuration

Create a `config.yaml` file (see Module 17.10 in curriculum for full example):

```yaml
llm:
  provider: anthropic  # or 'openai' or 'ollama'
  
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-3-5-sonnet-20241022
    temperature: 0.7
    max_tokens: 2000
```

### Environment Variables

Create a `.env` file (NEVER commit this file):

```bash
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Social Media APIs
X_BEARER_TOKEN=...
X_API_KEY=...
X_API_SECRET=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...

# Blockchain
INFURA_PROJECT_ID=...
ALCHEMY_API_KEY=...

# Private Keys (NEVER SHARE THESE)
# TRADING_WALLET_PRIVATE_KEY=...  # Only for testnets!
```

---

## 📚 How to Use These Examples

### For Students

1. **Start with the Simple Bot** (`06-trading-bot-simple.py`)
   - Understand the basic flow: data → analysis → decision → execution
   - Modify the RSI thresholds and see how it affects decisions
   - Add your own indicators

2. **Explore the LLM Framework** (`05-llm-agnostic-framework.py`)
   - Run with different providers (OpenAI, Anthropic, Ollama)
   - Compare response quality and costs
   - Add your own tools

3. **Add Sentiment Analysis** (`02-social-sentiment-analysis.py`)
   - Set up X and Reddit API access
   - Analyze sentiment for different cryptocurrencies
   - Integrate sentiment into your trading decisions

4. **Combine Multiple Sources** (`03-multi-source-decision-engine.py`)
   - See how professional traders combine signals
   - Adjust weights based on your research
   - Backtest different weighting schemes

5. **Integrate Blockchain Data** (`04-blockchain-defi-integration.py`)
   - Monitor whale wallets
   - Track DEX prices
   - **Test on testnets first!**

### For Instructors

- Use these as **live coding demonstrations**
- Assign sections as **homework** for students to modify and extend
- Create **coding challenges** based on these examples
- Use as **reference implementations** for student projects

---

## 🎯 Learning Objectives

By studying and working with these code examples, students will:

1. ✅ Understand AI agent architecture and implementation
2. ✅ Learn to integrate multiple data sources
3. ✅ Build LLM-agnostic applications
4. ✅ Implement trading algorithms with AI assistance
5. ✅ Work with blockchain data and smart contracts
6. ✅ Apply proper error handling and logging
7. ✅ Follow software engineering best practices

---

## ⚠️  Important Warnings

### Security
- **Never commit API keys or private keys to version control**
- Use environment variables for all secrets
- Enable IP whitelisting on exchange APIs
- Use read-only API keys when possible

### Trading
- **Start with paper trading (simulation)**
- Test extensively on testnets before using mainnet
- Never invest more than you can afford to lose
- Understand that AI can make mistakes

### Development
- Always handle API errors gracefully
- Respect API rate limits
- Log all decisions for debugging
- Test edge cases and failure scenarios

---

## 🔧 Customization Guide

### Adding a New LLM Provider

1. Create a new class inheriting from `BaseAgent`
2. Implement `generate()` and `get_cost_per_token()`
3. Add to the provider factory
4. Update `config.yaml`

### Adding a New Data Source

1. Create an async fetch method
2. Add to `DataGatheringPipeline.gather_all_data()`
3. Create a processing method
4. Update the decision engine to use the new data

### Adding a New Technical Indicator

1. Implement the calculation function
2. Add to the technical analysis section
3. Register as a tool for the AI agent
4. Update prompts to use the new indicator

---

## 📖 Related Curriculum Sections

- **Module 17.1:** Introduction to AI Agent Development
- **Module 17.2:** AI-Powered Application Development
- **Module 17.3:** Data Gathering & Information Synthesis
- **Module 17.4:** Social Media Sentiment Analysis
- **Module 17.5:** Building Your First AI Trading Bot
- **Module 17.6:** Multi-Source Decision Making
- **Module 17.7:** Blockchain & DeFi Integration
- **Module 17.8:** Trading Bot Fundamentals
- **Module 17.9:** Risk Management & Safety
- **Module 17.10:** LLM-Agnostic Framework Implementation
- **Module 17.11:** Student Customization Guide

---

## 🤝 Contributing

Students are encouraged to:
- Improve the code
- Add new features
- Fix bugs
- Share their modifications with the class

---

## 📞 Support

If you encounter issues:
1. Check the curriculum for conceptual explanations
2. Review the code comments
3. Ask your instructor
4. Consult the official documentation for APIs you're using

---

## 🎓 Assignment Ideas

1. **Beginner:** Modify the simple bot to use MACD instead of RSI
2. **Intermediate:** Add news sentiment analysis to the decision engine
3. **Advanced:** Implement a multi-agent system with specialized agents
4. **Expert:** Build a backtesting framework and optimize strategy parameters

---

**Remember:** These examples are for educational purposes. Real trading requires much more sophistication, testing, and risk management. Always start small and never risk money you can't afford to lose.

Good luck with your AI agent development journey! 🚀

