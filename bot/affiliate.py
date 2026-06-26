"""Turn a plain product URL into YOUR affiliate link (you earn the commission)."""
import config


def affiliate_link(url: str) -> str:
    tag = config.AMAZON_ASSOC_TAG
    if not tag or "tag=" in url:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}tag={tag}"
