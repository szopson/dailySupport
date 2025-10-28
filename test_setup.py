#!/usr/bin/env python3
"""
Test script for Morning Brief - Run this to verify everything works!
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_vars():
    """Test if all required environment variables are set"""
    print("🔍 Testing environment variables...")
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID',
        'TWITTER_BEARER_TOKEN',
        'COINGECKO_PRO_API_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            print(f"  ❌ {var}: NOT SET")
        else:
            value = os.getenv(var)
            masked = value[:10] + "..." if len(value) > 10 else "***"
            print(f"  ✅ {var}: {masked}")
    
    if missing:
        print(f"\n⚠️  Missing variables: {', '.join(missing)}")
        return False
    else:
        print("\n✅ All environment variables set!\n")
        return True

def test_telegram():
    """Test Telegram bot connection"""
    print("📱 Testing Telegram bot...")
    import requests
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # Test bot info
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        bot_info = response.json()
        
        if bot_info.get('ok'):
            bot_name = bot_info['result']['username']
            print(f"  ✅ Bot connected: @{bot_name}")
            
            # Send test message
            send_url = f"https://api.telegram.org/bot{token}/sendMessage"
            test_msg = "🧪 Test message from Morning Brief setup!\n\nIf you see this, everything is working! 🎉"
            
            data = {
                'chat_id': chat_id,
                'text': test_msg
            }
            
            send_response = requests.post(send_url, data=data, timeout=10)
            send_response.raise_for_status()
            
            if send_response.json().get('ok'):
                print(f"  ✅ Test message sent to chat ID: {chat_id}")
                return True
            else:
                print(f"  ❌ Failed to send message: {send_response.text}")
                return False
        else:
            print(f"  ❌ Bot authentication failed: {bot_info}")
            return False
            
    except Exception as e:
        print(f"  ❌ Telegram test failed: {e}")
        return False

def test_twitter():
    """Test Twitter API connection"""
    print("\n🐦 Testing Twitter API...")
    import tweepy
    
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        
        # Test by getting a known user
        user = client.get_user(username='elonmusk')
        
        if user.data:
            print(f"  ✅ Twitter API connected")
            print(f"  ✅ Test query successful (found @{user.data.username})")
            return True
        else:
            print(f"  ❌ Twitter API test failed: No data returned")
            return False
            
    except Exception as e:
        print(f"  ❌ Twitter test failed: {e}")
        return False

def test_coingecko():
    """Test CoinGecko API connection"""
    print("\n💰 Testing CoinGecko API...")
    import requests
    
    api_key = os.getenv('COINGECKO_PRO_API_KEY')
    
    url = "https://pro-api.coingecko.com/api/v3/ping"
    headers = {
        'X-Cg-Pro-Api-Key': api_key
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Test actual price fetch
        price_url = "https://pro-api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd'
        }
        
        price_response = requests.get(price_url, params=params, headers=headers, timeout=10)
        price_response.raise_for_status()
        
        btc_price = price_response.json()['bitcoin']['usd']
        print(f"  ✅ CoinGecko API connected")
        print(f"  ✅ BTC Price: ${btc_price:,.0f}")
        return True
        
    except Exception as e:
        print(f"  ❌ CoinGecko test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 MORNING BRIEF - SYSTEM TEST")
    print("="*60)
    print()
    
    results = []
    
    # Test environment variables
    results.append(("Environment Variables", test_env_vars()))
    
    if results[0][1]:  # Only continue if env vars are set
        # Test each service
        results.append(("Telegram Bot", test_telegram()))
        results.append(("Twitter API", test_twitter()))
        results.append(("CoinGecko API", test_coingecko()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the morning brief.")
        print("\nNext steps:")
        print("1. Run: python morning_brief.py")
        print("2. Check your Telegram for the morning brief")
        print("3. Set up GitHub Actions for automation (see SETUP.md)")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("- Verify API keys in .env file")
        print("- Make sure you've started a chat with your Telegram bot")
        print("- Check your internet connection")
        print("- Verify CoinGecko Pro subscription is active")
    
    print()

if __name__ == "__main__":
    main()
