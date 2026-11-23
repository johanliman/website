#!/usr/bin/env python3
"""
Fetch current market prices for stock portfolio tickers using Yahoo Finance API.
Outputs clean JSON to assets/data/stock-prices.json for web consumption.
"""

import os
import re
import json
import ssl
import time
import datetime
import urllib.request
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "assets", "data", "stock-prices.json")
HTML_FILE = os.path.join(BASE_DIR, "pages", "stock.html")

DEFAULT_TICKERS = [
    # Active portfolio holdings first
    "MSTR", "PLTR", "HOOD", "HIMS", "NFLX", "BABA", "NOW", "MARA", "CZR", "OSCR", "SOFI",
    # Watchlist / common tickers
    "AAPL", "NVDA", "MSFT", "TSLA", "AMZN", "GOOGL", "META", "AMD", "COIN", "SMCI", "INTC", "SPY", "QQQ"
]

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

def load_existing_prices():
    """Load existing prices to prevent wiping if a quote is temporarily throttled."""
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("prices", {}), data.get("details", {})
        except Exception:
            pass
    return {}, {}

def extract_tickers():
    """Extract tickers from HTML and default list."""
    tickers = list(DEFAULT_TICKERS)
    if os.path.exists(HTML_FILE):
        try:
            with open(HTML_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            found = re.findall(r'symbol:\s*["\']([A-Z0-9.\-]+)["\']', content, re.IGNORECASE)
            for s in found:
                sym = s.upper()
                if sym not in tickers:
                    tickers.insert(0, sym)
        except Exception as e:
            print(f"Warning parsing HTML: {e}")
    return tickers

def fetch_single_ticker(ticker, ctx, max_retries=2):
    """Fetch single ticker with retry and backoff."""
    hosts = ["query2.finance.yahoo.com", "query1.finance.yahoo.com"]

    for attempt in range(max_retries + 1):
        host = hosts[attempt % len(hosts)]
        url = f"https://{host}/v8/finance/chart/{ticker}?interval=1d&range=1d"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json"
        }
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=6) as response:
                data = json.loads(response.read().decode("utf-8"))
                result = data.get("chart", {}).get("result", [])
                if result:
                    meta = result[0].get("meta", {})
                    regular_price = meta.get("regularMarketPrice")
                    prev_close = meta.get("chartPreviousClose") or meta.get("previousClose")
                    if regular_price is not None:
                        regular_price = round(float(regular_price), 2)
                        prev_close = round(float(prev_close), 2) if prev_close else regular_price
                        change = round(regular_price - prev_close, 2)
                        change_pct = round((change / prev_close) * 100, 2) if prev_close > 0 else 0.0
                        return ticker, {
                            "price": regular_price,
                            "previousClose": prev_close,
                            "change": change,
                            "changePercent": change_pct
                        }
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                time.sleep(1.0 + attempt * 1.5)
                continue
            print(f"[{ticker}] HTTP Error {e.code}")
        except Exception as e:
            if attempt < max_retries:
                time.sleep(0.5)
                continue
            print(f"[{ticker}] Error: {e}")

    return ticker, None

def main():
    tickers = extract_tickers()
    print(f"Targeting {len(tickers)} tickers: {', '.join(tickers)}")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    existing_prices, existing_details = load_existing_prices()
    price_map = dict(existing_prices)
    details_map = dict(existing_details)

    success_count = 0
    t0 = time.time()

    for i, ticker in enumerate(tickers):
        ticker, info = fetch_single_ticker(ticker, ctx)
        if info:
            price_map[ticker] = info["price"]
            details_map[ticker] = info
            success_count += 1
            print(f"  ✓ {ticker}: ${info['price']:.2f} ({info['changePercent']:+.2f}%)")
        else:
            if ticker in price_map:
                print(f"  ⚠ {ticker}: Retained previous price ${price_map[ticker]:.2f}")
            else:
                print(f"  ✗ {ticker}: No quote available")
        # Polite spacing to avoid Yahoo rate limits
        time.sleep(0.2)

    elapsed = time.time() - t0
    print(f"Fetched {success_count}/{len(tickers)} new quotes in {elapsed:.2f}s (Total stored: {len(price_map)})")

    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "updated_at": now.isoformat(),
        "updated_timestamp": int(now.timestamp()),
        "count": len(price_map),
        "prices": price_map,
        "details": details_map
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Saved live stock data to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
