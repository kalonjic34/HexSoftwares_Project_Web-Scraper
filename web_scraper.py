from __future__ import annotations
import requests
from bs4 import BeautifulSoup
import csv
import json


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
        site_el = row.select_one(".sitestr")
        items.append({
            "rank": int(rank_el.get_text(strip=True).strip(".")) if rank_el else None,
            "title": title_el.get_text(strip=True) if title_el else None,
            "url": title_el.get("href") if title_el else None,
            "site": site_el.get_text(strip=True) if site_el else None,
        })
        return items

def save_csv(records: list[dict], path:str):
    if not records:
        with open(path, "w", newline="", encoding="utf=8")as f:
            f.write("")
        return
    keys = sorted({k for r in records for k in r.keys()})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in records:
            w.writerow(r)

def save_json(records: list[dict], path:str):
    with open(path, "w", encoding="utf-8")as f:
        json.dump(records,f,ensure_ascii=False, indent=2)
def main():
    print("Fetching Hacker News...")
    html = fetch_html("https://news.ycombinator.com/")
    data = parse_hackernews(html)
    print(f"Parsed {len(data)} items")
    for d in data[:3]:
        print("-",d["rank"], d["title"])
    
if __name__ == "__main__":
    main()