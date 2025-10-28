#!/usr/bin/env python3
"""
Morning Brief Automation for Crypto Portfolio
Sends daily briefing to Telegram at 7:00 AM Europe/Berlin time
"""

import os
import tweepy
import requests
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TIMEZONE = pytz.timezone(os.getenv('TIMEZONE', 'Europe/Berlin'))
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Twitter API Setup
twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
twitter_client = tweepy.Client(bearer_token=twitter_bearer_token)

# Your X Watchlist
X_ACCOUNTS = [
    'cryptomacavalli',   # general overview
    'Drewniany78',       # early degen bets
    'Cryptoo_Gems',      # early degen bets
    'gem_insider',       # early degen bets
    'CrypticTrades_',    # overview
    'astronomer_zero',   # overview
    'ero_crypto'         # early bets + trading ideas
]

# Your Portfolio
PORTFOLIO = {
    'main_holdings': [
        {'symbol': 'PEAQ', 'name': 'peaq', 'weight': 18.11},
        {'symbol': 'FET', 'name': 'Artificial Superintelligence Alliance', 'weight': 16.82},
        {'symbol': 'TAO', 'name': 'Bittensor', 'weight': 13.58},
        {'symbol': 'ORAI', 'name': 'Oraichain', 'weight': 10.39},
        {'symbol': 'ATH', 'name': 'Aethir', 'weight': 9.45},
        {'symbol': 'OVR', 'name': 'Ovr', 'weight': 8.11},
        {'symbol': 'VELO', 'name': 'Velo', 'weight': 6.0},
        {'symbol': 'ZIG', 'name': 'ZIGChain', 'weight': 5.87},
        {'symbol': 'LYX', 'name': 'LUKSO', 'weight': 5.04},
        {'symbol': 'VVV', 'name': 'Venice Token', 'weight': 3.55}
    ],
    'degen_plays': [
        'BREW/SOL', 'OPENX/WETH', 'Qstay/SOL', 
        'SHADY/SOL', 'WONDER/SOL', 'AVICI/USDC', 'BLAI/USDC'
    ]
}

def get_coingecko_ids():
    """Map symbols to CoinGecko IDs"""
    mapping = {
        'PEAQ': 'peaq',
        'FET': 'fetch-ai',
        'TAO': 'bittensor',
        'ORAI': 'oraichain-token',
        'ATH': 'aethir',
        'OVR': 'ovr',
        'VELO': 'velo',
        'ZIG': 'zignaly',
        'LYX': 'lukso-token',
        'VVV': 'venice-token'
    }
    return mapping

def fetch_twitter_feed(hours=24):
    """Fetch tweets from watchlist accounts in the last 24 hours"""
    tweets_by_account = {}
    cutoff_time = datetime.now(TIMEZONE) - timedelta(hours=hours)
    
    for username in X_ACCOUNTS:
        try:
            # Get user ID
            user = twitter_client.get_user(username=username)
            if not user.data:
                continue
                
            user_id = user.data.id
            
            # Get recent tweets
            tweets = twitter_client.get_users_tweets(
                id=user_id,
                max_results=10,
                tweet_fields=['created_at', 'public_metrics', 'text'],
                exclude=['retweets', 'replies']
            )
            
            if tweets.data:
                recent_tweets = [
                    {
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'likes': tweet.public_metrics['like_count'],
                        'retweets': tweet.public_metrics['retweet_count']
                    }
                    for tweet in tweets.data
                    if tweet.created_at > cutoff_time
                ]
                
                if recent_tweets:
                    tweets_by_account[username] = recent_tweets
                    
        except Exception as e:
            print(f"Error fetching tweets from {username}: {e}")
            
    return tweets_by_account

def fetch_portfolio_prices():
    """Fetch current prices for portfolio tokens using CoinGecko Pro"""
    api_key = os.getenv('COINGECKO_PRO_API_KEY')
    ids_map = get_coingecko_ids()
    
    # Get all CoinGecko IDs
    coin_ids = ','.join(ids_map.values())
    
    url = f"https://pro-api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': coin_ids,
        'vs_currencies': 'usd',
        'include_24hr_change': 'true',
        'include_24hr_vol': 'true'
    }
    headers = {
        'X-Cg-Pro-Api-Key': api_key
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Map back to our symbols
        portfolio_data = {}
        for symbol, cg_id in ids_map.items():
            if cg_id in data:
                portfolio_data[symbol] = {
                    'price': data[cg_id]['usd'],
                    'change_24h': data[cg_id].get('usd_24h_change', 0),
                    'volume_24h': data[cg_id].get('usd_24h_vol', 0)
                }
        
        return portfolio_data
        
    except Exception as e:
        print(f"Error fetching portfolio prices: {e}")
        return {}

def fetch_market_overview():
    """Fetch BTC, ETH and market overview"""
    api_key = os.getenv('COINGECKO_PRO_API_KEY')
    
    url = "https://pro-api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum',
        'vs_currencies': 'usd',
        'include_24hr_change': 'true',
        'include_market_cap': 'true'
    }
    headers = {
        'X-Cg-Pro-Api-Key': api_key
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        market_data = {
            'btc': {
                'price': data['bitcoin']['usd'],
                'change_24h': data['bitcoin']['usd_24h_change'],
                'market_cap': data['bitcoin']['usd_market_cap']
            },
            'eth': {
                'price': data['ethereum']['usd'],
                'change_24h': data['ethereum']['usd_24h_change'],
                'market_cap': data['ethereum']['usd_market_cap']
            }
        }
        
        return market_data
        
    except Exception as e:
        print(f"Error fetching market overview: {e}")
        return {}

def analyze_tweets(tweets_by_account):
    """Extract key insights from tweets"""
    insights = []
    
    for username, tweets in tweets_by_account.items():
        # Sort by engagement (likes + retweets)
        sorted_tweets = sorted(
            tweets,
            key=lambda x: x['likes'] + x['retweets'],
            reverse=True
        )
        
        # Take top tweet if it has decent engagement
        if sorted_tweets and (sorted_tweets[0]['likes'] + sorted_tweets[0]['retweets']) > 10:
            top_tweet = sorted_tweets[0]
            insights.append({
                'account': username,
                'text': top_tweet['text'][:200],  # Truncate
                'engagement': top_tweet['likes'] + top_tweet['retweets']
            })
    
    return insights

def format_morning_brief(market_data, portfolio_data, tweet_insights):
    """Format the morning brief message"""
    now = datetime.now(TIMEZONE)
    
    message = f"🌅 **Morning Brief - {now.strftime('%A, %B %d, %Y')}**\n\n"
    
    # Market Overview
    message += "📊 **Market Summary**\n"
    if market_data:
        btc = market_data.get('btc', {})
        eth = market_data.get('eth', {})
        
        btc_emoji = "🟢" if btc.get('change_24h', 0) > 0 else "🔴"
        eth_emoji = "🟢" if eth.get('change_24h', 0) > 0 else "🔴"
        
        message += f"{btc_emoji} BTC: ${btc.get('price', 0):,.0f} ({btc.get('change_24h', 0):+.2f}%)\n"
        message += f"{eth_emoji} ETH: ${eth.get('price', 0):,.0f} ({eth.get('change_24h', 0):+.2f}%)\n\n"
    
    # Portfolio Watch
    message += "💼 **Your Portfolio Watch**\n"
    if portfolio_data:
        for holding in PORTFOLIO['main_holdings'][:5]:  # Top 5 holdings
            symbol = holding['symbol']
            if symbol in portfolio_data:
                data = portfolio_data[symbol]
                emoji = "🟢" if data['change_24h'] > 0 else "🔴"
                message += f"{emoji} {symbol}: ${data['price']:.4f} ({data['change_24h']:+.2f}%)\n"
    message += "\n"
    
    # X Feed Digest
    message += "🐦 **X Feed Highlights**\n"
    if tweet_insights:
        for insight in tweet_insights[:3]:  # Top 3 tweets
            message += f"@{insight['account']} ({insight['engagement']} 💬):\n"
            message += f"{insight['text']}...\n\n"
    else:
        message += "No high-engagement tweets in last 24h\n\n"
    
    # Portuguese Lesson Reminder
    message += "🇵🇹 **Portuguese Lesson**\n"
    message += "15-minute lesson ready! Ask Claude for today's lesson.\n\n"
    
    # Day Priorities
    message += "📅 **Day Priorities**\n"
    message += "1. Check portfolio positioning\n"
    message += "2. Review X feed for alpha\n"
    message += "3. Gym session\n\n"
    
    message += "_Chat with Claude for deeper analysis! 💬_"
    
    return message

def send_telegram_message(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"✅ Message sent successfully at {datetime.now(TIMEZONE)}")
        return True
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def run_morning_brief():
    """Main function to generate and send morning brief"""
    print(f"🚀 Starting morning brief generation at {datetime.now(TIMEZONE)}")
    
    # Fetch data
    print("📱 Fetching Twitter feed...")
    tweets = fetch_twitter_feed(hours=24)
    
    print("📊 Fetching market data...")
    market_data = fetch_market_overview()
    
    print("💼 Fetching portfolio prices...")
    portfolio_data = fetch_portfolio_prices()
    
    print("🤔 Analyzing tweets...")
    tweet_insights = analyze_tweets(tweets)
    
    print("📝 Formatting message...")
    message = format_morning_brief(market_data, portfolio_data, tweet_insights)
    
    print("📤 Sending to Telegram...")
    success = send_telegram_message(message)
    
    if success:
        print("✅ Morning brief completed successfully!")
    else:
        print("❌ Morning brief failed to send")
    
    return success

if __name__ == "__main__":
    run_morning_brief()
