"""Write a catchy Telegram deal caption with Gemini (free), with a safe fallback."""
import time
import requests
import config

MODELS = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"]


def _gemini(prompt: str) -> str:
    if not config.GEMINI_API_KEY:
        return ""
    for attempt in range(2):
        for model in MODELS:
            url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{model}:generateContent?key={config.GEMINI_API_KEY}")
            try:
                r = requests.post(url, timeout=40,
                                  json={"contents": [{"parts": [{"text": prompt}]}]})
                if r.status_code == 200:
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                if r.status_code in (429, 503):
                    continue
            except Exception as ex:
                print(f"[caption] {model} error: {ex}")
        if attempt == 0:
            time.sleep(3)
    return ""


def make_caption(title: str) -> str:
    prompt = (
        f"Write a short, exciting Telegram deal-channel caption (Hindi + English mix) "
        f"for this product: '{title}'. 2-3 lines, 1-2 emojis, create genuine urgency "
        f"(limited-time / best price) WITHOUT inventing a specific price or fake discount. "
        f"End with a line like 'Abhi grab karo 👇'. Plain text only, no markdown."
    )
    text = _gemini(prompt)
    if not text:
        text = f"🔥 {title} — aaj ka best deal!\nLimited time offer. Abhi grab karo 👇"
    return text
