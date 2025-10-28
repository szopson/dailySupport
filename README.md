# 🌅 Crypto Morning Brief - Automated Daily Digest

**Get your personalized crypto morning brief delivered to Telegram every day at 7 AM!**

## 📬 What You Get Daily

- 📊 BTC/ETH market snapshot
- 💼 Your portfolio tokens (prices + 24h changes)
- 🐦 Best tweets from your 7 watchlist accounts
- 🇵🇹 Portuguese lesson reminder
- 📅 Daily priorities

**Plus:** Chat with Claude anytime for deeper analysis!

---

## ⚡ Quick Start (5 Minutes)

### 1️⃣ Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run test to verify everything works
python test_setup.py

# If tests pass, run the morning brief
python morning_brief.py
```

You should get a Telegram message! ✅

### 2️⃣ Set Up Automation (Optional)

Want it to run automatically every morning? See **[SETUP.md](SETUP.md)** for detailed instructions.

**Quick version:**
1. Create a private GitHub repo
2. Upload these files
3. Add API keys as GitHub Secrets
4. Enable GitHub Actions

That's it! Free automation via GitHub Actions.

---

## 📁 Files Overview

```
crypto-morning-brief/
├── morning_brief.py          # Main script
├── test_setup.py              # Test everything works
├── requirements.txt           # Python dependencies
├── .env                       # Your API keys (DON'T COMMIT!)
├── .gitignore                 # Protects .env file
├── SETUP.md                   # Detailed setup guide
├── README.md                  # This file
└── .github/
    └── workflows/
        └── morning-brief.yml  # GitHub Actions automation
```

---

## 🎯 Your Configuration

### Portfolio Tracked (10 main + 7 degen):
- PEAQ (18.11%), FET (16.82%), TAO (13.58%), ORAI (10.39%), ATH (9.45%)
- OVR (8.11%), VELO (6.0%), ZIG (5.87%), LYX (5.04%), VVV (3.55%)
- Plus: BREW, OPENX, Qstay, SHADY, WONDER, AVICI, BLAI

### X Watchlist (7 accounts):
- @cryptomacavalli - general overview
- @Drewniany78 - early degen bets
- @Cryptoo_Gems - early degen bets
- @gem_insider - early degen bets
- @CrypticTrades_ - overview
- @astronomer_zero - overview
- @ero_crypto - early bets + trading ideas

---

## 🛠️ Customization

### Change Schedule
Edit `.github/workflows/morning-brief.yml`:
```yaml
- cron: '0 6 * * *'  # 6 AM UTC = 7 AM Berlin
```

### Add Tokens
Edit `morning_brief.py` line 37

### Change X Accounts
Edit `morning_brief.py` line 28

---

## 💰 Cost

**Totally Free!**
- GitHub Actions: 2,000 minutes/month free (you'll use ~30)
- Twitter API: 10,000 tweets/month free (you'll use ~2,100)
- Telegram: Free forever
- Your existing CoinGecko Pro: Already have it

---

## 🔒 Security

- ✅ `.env` file is gitignored (never commit it!)
- ✅ API keys stored as GitHub Secrets
- ✅ Keep repository private
- ✅ Enable 2FA on GitHub

---

## 🐛 Troubleshooting

**"Test failed"**
- Check your API keys in `.env` file
- Make sure you've messaged your Telegram bot first
- Run: `python test_setup.py` for detailed diagnostics

**"No Telegram message"**
- Verify bot token is correct
- Start a chat with your bot on Telegram
- Check chat ID is correct

**"Twitter API error"**
- Verify bearer token is correct
- Check you haven't hit rate limits
- Try manually: visit twitter.com to confirm API is up

---

## 📞 Need Help?

1. Run `python test_setup.py` to diagnose issues
2. Check GitHub Actions logs if automation fails
3. See [SETUP.md](SETUP.md) for detailed troubleshooting
4. Ask Claude for help! 💬

---

## 🚀 Next Steps

1. ✅ Run `python test_setup.py`
2. ✅ Run `python morning_brief.py`
3. ✅ Set up GitHub Actions (see SETUP.md)
4. ✅ Wait for 7 AM tomorrow!
5. 🎉 Enjoy your automated morning brief!

---

**Built with:** Python, Twitter API, CoinGecko Pro, Telegram Bot API, GitHub Actions

**Maintained by:** You + Claude 🤖
