import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from scrapers import (
    scrape_price_nike,
    scrape_price_ebay,
    scrape_price_footlocker,
    scrape_price_marshalls,
    scrape_price_tjmaxx
)

# ── Whitelisted Scrapers ──────────────
SCRAPER_MAP = {
    "nike.com": scrape_price_nike,
    "ebay.com": scrape_price_ebay,
    "footlocker.com": scrape_price_footlocker,
    "marshalls.com": scrape_price_marshalls,
    "tjmaxx.tjx.com": scrape_price_tjmaxx,
}

# ── Product Page Filter ───────────────
def is_valid_product_page(link, domain):
    path = urlparse(link).path

    if domain == "nike.com":
        # Must be a direct product page (e.g., /t/air-force-1-07-white-black...)
        return path.startswith("/t/")
    
    elif domain == "ebay.com":
        # Product pages have /itm/ in the path (e.g., /itm/123456...)
        return "/itm/" in path

    elif domain == "footlocker.com":
        # Product pages start with /product/ (e.g., /product/nike-zoom-gt-jump/)
        return path.startswith("/product/")

    elif domain == "marshalls.com":
        # Marshalls product pages are under /us/store/jump/product/...
        return "/jump/product/" in path

    elif domain == "tjmaxx.tjx.com":
        # TJ Maxx follows the same /jump/product/ structure as Marshalls
        return "/jump/product/" in path

    return False

# ── DuckDuckGo Search Function ────────
def search_duckduckgo(query, max_results=5):
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    preferred_results = []
    fallback_results = []

    for a in soup.select("a.result__a"):
        title = a.get_text()
        raw_link = a["href"]

        # Extract real URL
        parsed = urlparse(raw_link)
        real_link = parse_qs(parsed.query).get("uddg", [raw_link])[0]
        domain = urlparse(real_link).netloc.replace("www.", "")

        result = {
            "title": title,
            "link": real_link,
            "price": None  # set later if preferred
        }

        # Check preferred domains
        if domain in SCRAPER_MAP and is_valid_product_page(real_link, domain):
            print(f"Checking {real_link} → {domain}")
            print("VALID PRODUCT PAGE?" , is_valid_product_page(real_link, domain))
            result["price"] = SCRAPER_MAP[domain](real_link)
            preferred_results.append(result)
        else:
            fallback_results.append(result)

        if len(preferred_results) >= (max_results - 1) and fallback_results:
            break

    # Always include one fallback result if available
    final_results = preferred_results[:max_results - 1]
    if fallback_results:
        final_results.append(fallback_results[0])

    return final_results



# ── Test Code ─────────────────────────
if __name__ == "__main__":
    query = "Nike Air Force 1 retail price"
    items = search_duckduckgo(query)
    for item in items:
        print(f"{item['title']} — {item['price']} — {item['link']}")
