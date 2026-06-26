"""Quickly add Amazon products to deals.json.

Usage (paste one or more Amazon URLs as arguments):
  python add_deal.py "https://www.amazon.in/dp/B08TV2P5HF" "https://www.amazon.in/dp/B0CMDRDR9D"

It auto-fetches each product's title (best-effort) and appends it as unposted.
Then commit:  git add deals.json && git commit -m "add deals" && git push
"""
import sys
import re
import json
import requests
import config

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}


def fetch_title(url: str) -> str:
    try:
        r = requests.get(url, headers=UA, timeout=20)
        m = re.search(r"<title>(.*?)</title>", r.text, re.S | re.I)
        if m:
            t = re.sub(r"\s+", " ", m.group(1)).strip()
            t = re.sub(r"(?i)\s*[:|-].*amazon.*$", "", t)   # drop 'Amazon.in' suffix
            t = re.sub(r"(?i)^amazon\.in[:\s]*", "", t)
            t = re.sub(r"(?i)^buy\s+", "", t)
            return t[:80].strip()
    except Exception as ex:
        print(f"  (title fetch failed: {ex})")
    return ""


def main():
    urls = sys.argv[1:]
    if not urls:
        print(__doc__)
        return
    data = json.loads(config.DEALS_FILE.read_text("utf-8"))
    existing = {d["url"] for d in data["deals"]}
    added = 0
    for u in urls:
        u = u.strip()
        if not u or u in existing:
            continue
        title = fetch_title(u) or "Amazon Deal - check it out"
        data["deals"].append({"title": title, "url": u, "posted": False})
        print(f"  + {title}")
        added += 1
    config.DEALS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    print(f"\nAdded {added} product(s) to deals.json.")
    print("Now run: git add deals.json && git commit -m \"add deals\" && git push")


if __name__ == "__main__":
    main()
