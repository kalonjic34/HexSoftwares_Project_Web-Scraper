from __future__ import annotations
import requests
from bs4 import BeautifulSoup
import csv
import json
import argparse
from typing import List, Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class ScrapeResult:
    records: List[dict]
    source_urls: List[str]
    

def fetch_html(url: str,timeout: int=20) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PersonalScraper/1.0; +https://example.local)"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text

def parse_hackernews(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    out: List[dict] = []
    for row in soup.select("tr.athing"):
        rank_el = row.select_one(".rank")
        title_el = row.select_one(".titleline a")
        site_el = row.select_one(".sitestr")
        sub = row.find_next_sibling("tr")
        points_el = sub.select_one(".score") if sub else None
        user_el = sub.select_one(".hnuser") if sub else None
        comments_text = ""
        if sub:
            links = sub.select("a")
            if links:
                comments_text = links[-1].get_text(strip=True)
        out.append({
            "rank": int(rank_el.get_text(strip=True).strip(".")) if rank_el else None,
            "title": title_el.get_text(strip=True) if title_el else None,
            "url": title_el.get("href") if title_el else None,
            "site": site_el.get_text(strip=True) if site_el else None,
            "points": _leading_int(points_el.get_text(strip=True) if points_el else ""),
            "author":user_el.get_text(strip=True) if user_el else None,
            "comments": _leading_int(comments_text),
        })
    return out

def _to_int(s:str) -> Optional[int]:
    try:
        return int(s)
    except Exception:
        return None

def _leading_int(s:str) -> int:
    num =""
    for ch in s:
        if ch.isdigit():
            num += ch
        elif num:
            break
    return int(num) if num else 0

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

def parse_args():
    p = argparse.ArgumentParser(description="Modular web scraper")
    p.add_argument("--site", help="Target site code (e.g., hn)")
    p.add_argument("--out", help="Output path (.csv or .json)")
    return p.parse_args()

def main():
    args = parse_args()
    print("Args:", vars(args))
    
if __name__ == "__main__":
    main()