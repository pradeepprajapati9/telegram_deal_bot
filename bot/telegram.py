"""Post a message to your Telegram channel via the Bot API (free)."""
import requests
import config


def post(text: str) -> bool:
    if not config.DO_POST:
        print("=== DRY-RUN (DO_POST=false) — would post: ===\n" + text + "\n")
        return True
    if not (config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHANNEL):
        print("[telegram] missing bot token / channel")
        return False
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, timeout=30, data={
            "chat_id": config.TELEGRAM_CHANNEL,
            "text": text,
            "disable_web_page_preview": False,   # show the product link preview/image
        })
        if r.status_code == 200 and r.json().get("ok"):
            print("[telegram] posted ✓")
            return True
        print(f"[telegram] failed: {r.status_code} {r.text[:200]}")
    except Exception as ex:
        print(f"[telegram] error: {ex}")
    return False
