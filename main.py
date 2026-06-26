"""Telegram deal/affiliate bot - posts one product deal per run.

  pick next unposted product -> build YOUR affiliate link -> Gemini caption
  -> post to your Telegram channel -> mark posted

Run on a schedule (GitHub Actions / Task Scheduler). With DO_POST=false it just
prints the post (safe dry-run) so you can review before going live.
"""
import sys
import json
import traceback
from datetime import datetime

import config
from bot import affiliate, caption, telegram

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def log(msg: str):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line)
    try:
        with open(config.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def _load():
    return json.loads(config.DEALS_FILE.read_text("utf-8"))


def _save(data):
    config.DEALS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


def run():
    data = _load()
    deals = data.get("deals", [])
    nxt = next((d for d in deals if not d.get("posted")), None)
    if not nxt:
        log("No unposted deals left. Add more products to deals.json.")
        return

    link = affiliate.affiliate_link(nxt["url"])
    cap = caption.make_caption(nxt["title"])
    message = f"{cap}\n\n🛒 {nxt['title']}\n👉 {link}"

    log(f"Posting deal: {nxt['title']}")
    if telegram.post(message):
        nxt["posted"] = True
        _save(data)
        log("Done.")
    else:
        log("Post failed (will retry this deal next run).")


if __name__ == "__main__":
    try:
        run()
    except Exception:
        log("ERROR:\n" + traceback.format_exc())
        sys.exit(1)
