"""
Module 17.4: Social Media Sentiment Analysis
Complete implementation for analyzing sentiment across X, Reddit, Discord, and Telegram

This demonstrates how to connect to social media APIs and perform sentiment analysis
on cryptocurrency discussions.
"""

import tweepy
import praw
import discord
from transformers import pipeline
from collections import Counter


# ============================================================================
# API SETUP
# ============================================================================

def setup_x_client(config: dict):
    """Set up X (Twitter) API client"""
    return tweepy.Client(
        bearer_token=config['bearer_token'],
        consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        access_token=config['access_token'],
        access_token_secret=config['access_secret']
    )


def setup_reddit_client(config: dict):
    """Set up Reddit API client"""
    return praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        user_agent="CryptoSentimentBot/1.0"
    )


def setup_discord_client():
    """Set up Discord bot client"""
    return discord.Client(intents=discord.Intents.default())


# ============================================================================
# DATA FETCHING
# ============================================================================

async def fetch_x_sentiment(x_client, symbol: str, hours: int = 24) -> list:
    """Fetch recent tweets about cryptocurrency"""
    query = f"#{symbol} OR ${symbol} -is:retweet lang:en"
    tweets = x_client.search_recent_tweets(
        query=query,
        max_results=100,
        tweet_fields=['created_at', 'public_metrics', 'author_id']
    )
    
    return [
        {
            'text': tweet.text,
            'likes': tweet.public_metrics['like_count'],
            'retweets': tweet.public_metrics['retweet_count'],
            'created_at': tweet.created_at
        }
        for tweet in tweets.data
    ]


async def fetch_reddit_sentiment(reddit_client, subreddit: str = "cryptocurrency", limit: int = 100) -> list:
    """Fetch recent Reddit posts"""
    sub = reddit_client.subreddit(subreddit)
    posts = sub.hot(limit=limit)
    
    return [
        {
            'title': post.title,
            'text': post.selftext,
            'score': post.score,
            'comments': post.num_comments,
            'upvote_ratio': post.upvote_ratio,
            'created_at': post.created_utc
        }
        for post in posts
    ]


# ============================================================================
# SENTIMENT ANALYSIS
# ============================================================================

# Option 1: Pre-trained finance model
sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")


def analyze_text_sentiment(text: str) -> dict:
    """Analyze sentiment of text using pre-trained model"""
    result = sentiment_analyzer(text[:512])[0]  # Limit to 512 tokens
    return {
        'label': result['label'],  # POSITIVE, NEGATIVE, NEUTRAL
        'score': result['score']    # Confidence 0-1
    }


# Option 2: LLM-based sentiment analysis (more nuanced)
async def analyze_with_llm(text: str, llm_client) -> dict:
    """Use AI to analyze sentiment with context understanding"""
    prompt = f"""
    Analyze the sentiment of this cryptocurrency-related text.
    Consider sarcasm, context, and market implications.
    
    Text: "{text}"
    
    Respond with:
    SENTIMENT: [BULLISH/BEARISH/NEUTRAL]
    CONFIDENCE: [1-10]
    REASONING: [Brief explanation]
    """
    
    response = await llm_client.generate(prompt)
    return parse_sentiment_response(response)


def parse_sentiment_response(response: str) -> dict:
    """Parse structured sentiment response"""
    # Simple parsing implementation
    lines = response.strip().split('\n')
    result = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    return result


# ============================================================================
# SENTIMENT AGGREGATION
# ============================================================================

class SentimentAggregator:
    """Combine sentiment from multiple sources with weighting"""
    
    def calculate_overall_sentiment(self, symbol: str, x_data: list, reddit_data: list) -> dict:
        """Calculate weighted sentiment score from multiple sources"""
        
        # Analyze each source
        x_sentiments = [analyze_text_sentiment(t['text']) for t in x_data]
        reddit_sentiments = [
            analyze_text_sentiment(p['title'] + " " + p['text']) 
            for p in reddit_data
        ]
        
        # Calculate weighted scores
        x_score = self._calculate_weighted_score(x_sentiments, x_data)
        reddit_score = self._calculate_weighted_score(reddit_sentiments, reddit_data)
        
        # Weight by source reliability (adjust based on your research)
        overall_score = (x_score * 0.4) + (reddit_score * 0.6)
        
        return {
            'overall_sentiment': overall_score,  # -1 to 1 scale
            'x_sentiment': x_score,
            'reddit_sentiment': reddit_score,
            'classification': self._classify_sentiment(overall_score),
            'confidence': self._calculate_confidence(x_data, reddit_data)
        }
    
    def _calculate_weighted_score(self, sentiments: list, data: list) -> float:
        """Weight sentiments by engagement (likes, upvotes, etc.)"""
        total_weight = 0
        weighted_sum = 0
        
        for sentiment, item in zip(sentiments, data):
            # Convert sentiment to numeric score
            score = 1 if sentiment['label'] == 'POSITIVE' else (-1 if sentiment['label'] == 'NEGATIVE' else 0)
            score *= sentiment['score']  # Multiply by confidence
            
            # Weight by engagement
            weight = item.get('likes', 0) + item.get('retweets', 0) + item.get('score', 0)
            weight = max(weight, 1)  # Minimum weight of 1
            
            weighted_sum += score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    def _classify_sentiment(self, score: float) -> str:
        """Convert numeric score to classification"""
        if score > 0.3:
            return "BULLISH"
        elif score < -0.3:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def _calculate_confidence(self, *data_sources) -> float:
        """Calculate confidence based on data volume"""
        total_items = sum(len(source) for source in data_sources)
        # More data = higher confidence
        confidence = min(total_items / 200, 1.0)  # Cap at 1.0
        return confidence


# ============================================================================
# TRENDING TOPICS
# ============================================================================

def detect_trending_topics(texts: list) -> list:
    """Find most mentioned topics in social media"""
    
    # Extract hashtags and cashtags
    hashtags = []
    for text in texts:
        hashtags.extend([word for word in text.split() if word.startswith('#') or word.startswith('$')])
    
    # Count frequency
    trending = Counter(hashtags).most_common(20)
    
    return [{'topic': topic, 'mentions': count} for topic, count in trending]


# ============================================================================
# INFLUENCER TRACKING
# ============================================================================

class InfluencerTracker:
    """Track sentiment from influential crypto accounts"""
    
    INFLUENTIAL_ACCOUNTS = [
        'VitalikButerin',
        'cz_binance',
        'elonmusk',
        # Add more influential accounts
    ]
    
    async def get_influencer_sentiment(self, x_client, symbol: str) -> dict:
        """Check what influencers are saying about a cryptocurrency"""
        
        sentiments = {}
        for username in self.INFLUENTIAL_ACCOUNTS:
            tweets = x_client.get_users_tweets(
                username=username,
                max_results=10
            )
            
            relevant_tweets = [t for t in tweets.data 
                             if symbol.lower() in t.text.lower()]
            
            if relevant_tweets:
                sentiment = analyze_text_sentiment(relevant_tweets[0].text)
                sentiments[username] = {
                    'sentiment': sentiment,
                    'text': relevant_tweets[0].text,
                    'timestamp': relevant_tweets[0].created_at
                }
        
        return sentiments

