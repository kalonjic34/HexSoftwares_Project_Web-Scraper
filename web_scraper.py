from __future__ import annotations
import requests
from bs4 import BeautifulSoup

def fetch_html(url: str,timeout: int=20) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PersonalScraper/1.0; +https://example.local)"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def parse_hackernews(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("tr.athing"):
        rank_el = row.select_one(".rank")
        title_el = row.select_one(".titleline a")
        items.append({
            "rank": int(rank_el.get_text(strip=True).strip(".")) if rank_el else None,
            "title": title_el.get_text(strip=True) if title_el else None,
            "url": title_el.get("href") if title_el else None,
        })
        return items

def main():
    print("Web Scraper starting...")
    
if __name__ == "__main__":
    main()