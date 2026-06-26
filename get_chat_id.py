"""Find your channel's chat_id reliably.

Steps:
  1. Make sure your bot is an ADMIN of the channel.
  2. Post any message in the channel (e.g. "test").
  3. Put the bot token in .env, then run:  python get_chat_id.py
It prints the channel's chat_id (a negative number like -1001234567890).
Use that as TELEGRAM_CHANNEL in .env.
"""
import requests
import config

if not config.TELEGRAM_BOT_TOKEN:
    print("Put TELEGRAM_BOT_TOKEN in .env first.")
    raise SystemExit(1)

r = requests.get(
    f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getUpdates", timeout=30)
data = r.json()

found = {}
for u in data.get("result", []):
    post = u.get("channel_post") or u.get("edited_channel_post") \
        or (u.get("my_chat_member") or {}).get("chat") and {"chat": u["my_chat_member"]["chat"]}
    chat = (u.get("channel_post") or u.get("edited_channel_post") or {}).get("chat") \
        or (u.get("my_chat_member") or {}).get("chat")
    if chat and chat.get("type") == "channel":
        found[chat["id"]] = chat.get("title", "")

if found:
    print("Channel(s) found:")
    for cid, title in found.items():
        print(f"  TELEGRAM_CHANNEL={cid}    ({title})")
else:
    print("No channel post found. Did you: (1) add the bot as admin, "
          "(2) post a message in the channel, then run this? Raw response:")
    print(data)
