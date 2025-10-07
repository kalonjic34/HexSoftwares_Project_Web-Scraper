from __future__ import annotations
import requests

def fetch_html(url: str,timeout: int=20) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PersonalScraper/1.0; +https://example.local)"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def main():
    print("Web Scraper starting...")
    
if __name__ == "__main__":
    main()