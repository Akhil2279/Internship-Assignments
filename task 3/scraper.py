#!/usr/bin/env python3
"""
scraper.py
A small, human-written web scraper that fetches news headlines from a page URL,
prints them to the terminal and (optionally) saves them to CSV.

Usage:
    python scraper.py https://www.bbc.com/news --max 15 --csv headlines.csv

Notes:
- This scraper uses a flexible approach to find headline-like elements.
- Use responsibly and respect a site's robots.txt and terms of service.
"""

import argparse
import csv
import sys
from typing import List, Set

import requests
from bs4 import BeautifulSoup, Tag

# Default user-agent (polite)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; NewsHeadlineScraper/1.0; +https://example.com/bot)"
}


def fetch_url(url: str, timeout: int = 10) -> requests.Response:
    """
    Fetch a URL and return the requests.Response object.
    Raises requests.exceptions.RequestException on network errors.
    """
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    return resp


def extract_headlines(html: str, max_items: int = 20) -> List[str]:
    """
    Extract likely headlines from HTML.
    Strategy:
    - Find common headline tags (h1, h2, h3).
    - Also check anchor tags that include headline-like classes.
    - Filter duplicates and very short texts.
    """
    soup = BeautifulSoup(html, "lxml")
    texts: List[str] = []
    seen: Set[str] = set()

    # Search for standard header tags first
    for tag_name in ("h1", "h2", "h3"):
        for tag in soup.find_all(tag_name):
            if isinstance(tag, Tag):
                text = tag.get_text(strip=True)
                if valid_headline(text):
                    if text not in seen:
                        texts.append(text)
                        seen.add(text)
                        if len(texts) >= max_items:
                            return texts

    # If not enough found, look for anchors with headline-like class names
    anchor_candidates = soup.find_all("a")
    for a in anchor_candidates:
        if isinstance(a, Tag):
            text = a.get_text(strip=True)
            classes = " ".join(a.get("class") or [])
            # Heuristic: many news sites use "title", "headline", "promo", "story"
            if valid_headline(text) and any(k in classes.lower() for k in ("title", "headline", "promo", "story", "heading")):
                if text not in seen:
                    texts.append(text)
                    seen.add(text)
                    if len(texts) >= max_items:
                        return texts

    # Last resort: collect any long, prominent text nodes from paragraphs or divs
    if len(texts) < max_items:
        candidates = soup.find_all(["p", "div", "span"])
        for c in candidates:
            if isinstance(c, Tag):
                text = c.get_text(strip=True)
                if valid_headline(text) and text not in seen:
                    texts.append(text)
                    seen.add(text)
                    if len(texts) >= max_items:
                        break

    return texts


def valid_headline(text: str, min_len: int = 15, max_len: int = 150) -> bool:
    """Simple filters to avoid tiny or trivial text."""
    if not text:
        return False
    text = " ".join(text.split())  # normalize whitespace
    if len(text) < min_len or len(text) > max_len:
        return False
    # Avoid purely numeric strings
    if text.isdigit():
        return False
    # Avoid texts that look like navigation labels (Home, Contact)
    nav_stopwords = {"home", "contact", "about", "privacy", "terms"}
    if text.strip().lower() in nav_stopwords:
        return False
    return True


def save_to_csv(filename: str, headlines: List[str]) -> None:
    """Save headlines to CSV file (one column 'headline')."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["headline"])
        for h in headlines:
            writer.writerow([h])


def main():
    parser = argparse.ArgumentParser(description="Simple News Headline Scraper")
    parser.add_argument("url", help="The page URL to scrape (e.g. https://www.bbc.com/news)")
    parser.add_argument("--max", type=int, default=20, help="Maximum number of headlines to extract")
    parser.add_argument("--csv", default="", help="If provided, save results to this CSV file")
    args = parser.parse_args()

    try:
        resp = fetch_url(args.url)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network or request failed: {e}", file=sys.stderr)
        sys.exit(2)

    # Check HTTP status code and handle non-200
    if resp.status_code != 200:
        print(f"[ERROR] Received HTTP status code {resp.status_code} for URL: {args.url}", file=sys.stderr)
        sys.exit(3)

    headlines = extract_headlines(resp.text, max_items=args.max)
    if not headlines:
        print("[WARN] No headlines detected with heuristics. Try a different URL or increase --max.", file=sys.stderr)
    else:
        print(f"Found {len(headlines)} headline(s):\n")
        for i, h in enumerate(headlines, start=1):
            print(f"{i:2d}. {h}")

    if args.csv and headlines:
        try:
            save_to_csv(args.csv, headlines)
            print(f"\nSaved {len(headlines)} headlines to: {args.csv}")
        except OSError as e:
            print(f"[ERROR] Could not write CSV: {e}", file=sys.stderr)
            sys.exit(4)


if __name__ == "__main__":
    main()
