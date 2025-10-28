# 🌅 Morning Brief Automation - Setup Guide

## 📋 Overview

This system sends you an automated morning brief every day at **7:00 AM Europe/Berlin time** via Telegram, including:
- 📊 BTC/ETH market overview
- 💼 Your portfolio token prices & 24h changes
- 🐦 Top tweets from your 7 watchlist accounts
- 🇵🇹 Portuguese lesson reminder
- 📅 Daily priorities

**Plus:** You can still chat with Claude anytime for deeper analysis!

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and create a new **private repository**
2. Name it something like `crypto-morning-brief`
3. Upload these files:
   - `morning_brief.py`
   - `requirements.txt`
   - `.github/workflows/morning-brief.yml`

### Step 2: Add GitHub Secrets

In your repository, go to **Settings → Secrets and variables → Actions** and add these secrets:

```
TELEGRAM_BOT_TOKEN = 8217120679:AAFdsqB4yslDwqANuiJ4M647EHfrhxzhvL0
TELEGRAM_CHAT_ID = 636594778
TWITTER_BEARER_TOKEN = AAAAAAAAAAAAAAAAAAAAAJs4zwEAAAAAdyZkXespQzpvinJ7aMbjXLHDZK8%3D3D4NTGBPePAuaJjA4gf4h3EFyAqzdTlCKdm0YzyB0qcNsEgkzo
COINGECKO_PRO_API_KEY = CG-aY1xBfK3wVo5qZzuaKcSunjt
```

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repo
2. Enable workflows
3. Click on "Morning Brief Automation"
4. Click "Run workflow" to test immediately

**That's it!** 🎉

---

## 🧪 Test Locally First

Before setting up automation, test it on your computer:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script
python morning_brief.py
```

You should receive a Telegram message within seconds!

---

## 📅 Schedule Details

**Default Schedule:** 7:00 AM Europe/Berlin (6:00 AM UTC)

The workflow runs using GitHub Actions cron:
- **Standard Time:** `0 6 * * *` (6 AM UTC = 7 AM Berlin)
- **Daylight Saving:** Adjust to `0 5 * * *` (5 AM UTC = 7 AM Berlin DST)

**Manual Trigger:** You can also run it anytime from GitHub Actions → "Run workflow"

---

## 🎛️ Customization Options

### Change Schedule Time

Edit `.github/workflows/morning-brief.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'  # Change the hour (0-23 UTC)
```

### Add/Remove X Accounts

Edit `morning_brief.py` line 28:

```python
X_ACCOUNTS = [
    'cryptomacavalli',
    'your_new_account',  # Add here
    # Remove any you don't want
]
```

### Add/Remove Portfolio Tokens

Edit `morning_brief.py` line 37:

```python
PORTFOLIO = {
    'main_holdings': [
        {'symbol': 'PEAQ', 'name': 'peaq', 'weight': 18.11},
        # Add or remove tokens here
    ]
}
```

### Change Message Format

Edit the `format_morning_brief()` function around line 180 to customize the Telegram message.

---

## 🔍 Monitoring & Troubleshooting

### Check if it's working:
1. Go to **Actions** tab in GitHub
2. Look for green checkmarks ✅
3. You should get a Telegram message every morning at 7 AM

### If something fails:
1. Check **Actions** tab for error logs
2. Verify your API keys are correct in GitHub Secrets
3. Test locally with `python morning_brief.py`
4. Check Telegram bot is working: send a message to it

### Common Issues:

**"Twitter API rate limit"**
- Free tier allows 10,000 tweets/month
- You're fetching ~70 tweets/day = ~2,100/month
- Should be fine, but if limited, reduce `max_results` in code

**"CoinGecko API error"**
- Pro plan has rate limits
- Script caches data to minimize calls
- Should be under limits easily

**"Telegram not sending"**
- Verify bot token is correct
- Make sure you've started a chat with the bot
- Test with: `curl "https://api.telegram.org/bot<TOKEN>/getMe"`

---

## 💰 Cost Breakdown

### Free:
- ✅ GitHub Actions (2,000 minutes/month free)
- ✅ Twitter API (10K tweets/month free)
- ✅ Telegram Bot (free)

### Paid:
- ✅ CoinGecko Pro: Already have ($129/month)
- ✅ All other APIs: Already have

**Total Additional Cost: $0** 🎉

---

## 🔐 Security Notes

1. **Never commit `.env` file** - it's in `.gitignore` already
2. **Keep repo private** - your API keys are in GitHub Secrets
3. **Rotate keys periodically** - especially Twitter API
4. **2FA on GitHub** - protect your repo access

---

## 📱 Telegram Bot Setup (If Needed)

If you ever need to recreate the bot:

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow instructions to get bot token
4. Send `/start` to your new bot to initialize chat
5. Get your chat ID by messaging the bot, then visiting:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```

---

## 🎯 Next Steps

### After Setup:

1. **Test it:** Run workflow manually to confirm it works
2. **Wait for 7 AM:** See if automated run works
3. **Adjust timing:** If needed, change cron schedule
4. **Customize:** Tweak the message format to your liking

### For Deeper Analysis:

Just chat with Claude anytime! Say:
- "Analyze PEAQ news"
- "What's the VELO outlook?"
- "Should I take profits on FET?"
- "Give me Portuguese lesson"

---

## 📞 Support

If something breaks or you need help:
1. Check GitHub Actions logs
2. Test locally first
3. Ask Claude for debugging help
4. Verify API keys haven't expired

---

## 🔄 Updates & Maintenance

### Weekly:
- Check GitHub Actions ran successfully
- Verify Telegram messages arriving

### Monthly:
- Review API usage (stay under limits)
- Update token list if portfolio changes
- Adjust X watchlist if needed

### As Needed:
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Adjust cron for DST changes
- Add new features!

---

## 🎨 Future Enhancements

Ideas to add later:
- 📈 Price alerts for big moves
- 🚨 Token unlock warnings
- 📰 News sentiment analysis
- 🤖 AI-generated trading insights
- 📊 Portfolio performance tracking
- 💬 Two-way Telegram commands

---

**You're all set!** 🚀

The system will now send you a morning brief every day at 7 AM, and you can chat with Claude anytime for deeper analysis.
