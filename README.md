# 🛒 Telegram Deal / Affiliate Bot

Auto-posts product deals to your Telegram channel with YOUR affiliate link.
When someone buys through it, you earn a commission — you never handle products,
delivery, or customers. Fully free + automated.

## How it works
```
deals.json (your products) -> add YOUR affiliate tag -> Gemini writes a catchy
caption -> post to your Telegram channel (on schedule) -> mark posted
```

## Setup

### 1. Telegram bot + channel
1. In Telegram, message **@BotFather** -> `/newbot` -> get the **bot token**.
2. Create a **channel** (public, pick a @username).
3. Add your bot as an **Admin** of the channel (so it can post).

### 2. Amazon Associates (free)
- Sign up at https://affiliate-program.amazon.in -> get your tag (e.g. `yourname-21`).
- (Or use EarnKaro/Cuelinks links instead — just paste those URLs into deals.json.)

### 3. Configure & test
```powershell
copy .env.example .env       # fill TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL, AMAZON_ASSOC_TAG, GEMINI_API_KEY
pip install -r requirements.txt
python main.py               # DO_POST=false -> dry-run preview
```
Happy with the preview? Set `DO_POST=true` and run again to post for real.

### 4. Automate (free, cloud)
Push to a GitHub repo, add the same values as **Actions secrets**
(`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL`, `AMAZON_ASSOC_TAG`, `GEMINI_API_KEY`).
`.github/workflows/post.yml` posts 3 deals/day automatically.

## Add more products
Edit `deals.json` — add `{"title": "...", "url": "https://...", "posted": false}`.
The bot posts one unposted deal per run.

## Your only job
Grow the channel (share it, get members). More members -> more clicks -> more sales.
