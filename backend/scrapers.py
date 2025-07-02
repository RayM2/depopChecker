import requests
from bs4 import BeautifulSoup

# ── Nike ─────────────────────────────
def scrape_price_nike(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        price_el = soup.select_one('span[data-testid="currentPrice-container"]')
        return price_el.text.strip() if price_el else "Price not found"
    except Exception as e:
        print(f"Error scraping Nike: {e}")
        return "Scrape error"

# ── eBay ─────────────────────────────
def scrape_price_ebay(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        price_el = soup.select_one('div[data-testid="x-price-primary"] span.ux-textspans')
        return price_el.text.strip() if price_el else "Price not found"
    except Exception as e:
        print(f"Error scraping eBay: {e}")
        return "Scrape error"
def scrape_price_footlocker(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        price_el = soup.select_one('div.ProductPrice span')
        return price_el.text.strip() if price_el else "Price not found"
    except Exception as e:
        print(f"Error scraping Footlocker: {e}")
        return "Scrape error"
    
def scrape_price_marshalls(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Find the actual sale price (first span.product-price inside <p class="price">)
        price_container = soup.select_one('p.price span.product-price')
        if price_container:
            return price_container.text.strip()
        return "Price not found"
    except Exception as e:
        print(f"Error scraping Marshalls: {e}")
        return "Scrape error"
def scrape_price_tjmaxx(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Try discounted price first
        discount_el = soup.select_one("span.discounted-price")
        if discount_el:
            text = discount_el.get_text(strip=True)
            return text.replace("new price:", "").strip()

        # Fallback if only one price is present
        price_el = soup.select_one("span.product-price")
        if price_el:
            return price_el.text.strip()

        return "Price not found"
    except Exception as e:
        print(f"Error scraping TJ Maxx: {e}")
        return "Scrape error"
