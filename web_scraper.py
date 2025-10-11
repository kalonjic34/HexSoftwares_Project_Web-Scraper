from __future__ import annotations
import requests
from bs4 import BeautifulSoup
import argparse
import csv
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

@dataclass
class ScrapeResult:
    records: List[dict]
    source_urls: List[str]


def fetch_html(url: str, timeout: int = 20) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PersonalScraper/1.0; +https://example.local)"
    }
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text


def parse_hackernews(html: str) -> List[dict]:
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
            "rank": _to_int(rank_el.get_text(strip=True).strip(".")) if rank_el else None,
            "title": title_el.get_text(strip=True) if title_el else None,
            "url": title_el.get("href") if title_el else None,
            "site": site_el.get_text(strip=True) if site_el else None,
            "points": _leading_int(points_el.get_text(strip=True) if points_el else ""),
            "author": user_el.get_text(strip=True) if user_el else None,
            "comments": _leading_int(comments_text),
        })
    return out


def parse_quotes_page(html: str) -> Tuple[List[dict], Optional[str]]:
    soup = BeautifulSoup(html, "html.parser")
    out: List[dict] = []
    for q in soup.select(".quote"):
        text = q.select_one(".text").get_text(strip=True)
        author = q.select_one(".author").get_text(strip=True)
        tags = [t.get_text(strip=True) for t in q.select(".tag")]
        out.append({"text": text, "author": author, "tags": tags})
    next_link = soup.select_one("li.next a")
    next_href = next_link.get("href") if next_link else None
    return out, next_href


def _to_int(s: str) -> Optional[int]:
    try:
        return int(s)
    except Exception:
        return None


def _leading_int(s: str) -> int:
    num = ""
    for ch in s:
        if ch.isdigit():
            num += ch
        elif num:
            break
    return int(num) if num else 0


def iter_pages_quotes(base_url: str, pages: int, delay: float) -> Iterable[str]:
    seen = 0
    url = base_url
    while url and (seen < pages):
        yield url
        seen += 1
        html = fetch_html(url)
        _, next_href = parse_quotes_page(html)
        if not next_href:
            break
        if next_href.startswith("http"):
            url = next_href
        else:
            url = base_url.rstrip("/") + next_href
        time.sleep(delay)


SCRAPE_TARGETS: Dict[str, Dict[str, Any]] = {
    "hn": {
        "name": "Hacker News (front page)",
        "urls": ["https://news.ycombinator.com/"],
        "supports_pages": False,
        "default_pages": 1,
        "fetch": lambda urls, pages, delay: urls,
        "parse": parse_hackernews,
        "fields_hint": ["rank", "title", "url", "site", "points", "author", "comments"],
    },
    "quotes": {
        "name": "Quotes to Scrape (paginated)",
        "urls": ["https://quotes.toscrape.com/"],
        "supports_pages": True,
        "default_pages": 2,
        "fetch": lambda urls, pages, delay: iter_pages_quotes(urls[0], pages, delay),
        "parse": lambda html: parse_quotes_page(html)[0],
        "fields_hint": ["text", "author", "tags"],
    },
}


def save_csv(records: List[dict], path: str):
    keys = set()
    for r in records:
        keys.update(r.keys())
    fieldnames = sorted(keys)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in records:
            w.writerow(r)

def save_json(records: List[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def run_scrape(site: str, out: str, pages: int, delay: float):
    meta = SCRAPE_TARGETS[site]
    if not meta["supports_pages"]:
        pages = 1

    records: List[dict] = []
    source_urls: List[str] = []

    url_iter = meta["fetch"](meta["urls"], pages, delay)
    idx = 0
    for url in url_iter:
        idx += 1
        print(f"[{idx}] Fetching {url}")
        html = fetch_html(url)
        source_urls.append(url)
        page_records = meta["parse"](html)
        print(f"    Parsed {len(page_records)} records")
        records.extend(page_records)
    if out.endswith(".csv"):
        save_csv(records, out)
    else:
        save_json(records, out)
    print(f"Saved {len(records)} records to {out}")
    return ScrapeResult(records=records, source_urls=source_urls)


def parse_args():
    p = argparse.ArgumentParser(description="Modular web scraper")
    p.add_argument("--site", choices=list(SCRAPE_TARGETS.keys()), required=True)
    p.add_argument("--out", required=True, help="Output path (.csv or .json)")
    p.add_argument("--pages", type=int, default=None, help="Number of pages to scrape")
    p.add_argument("--delay", type=float, default=0.8, help="Delay between requests (seconds)")
    return p.parse_args()

def prompt_menu():
    print("Web Scraper")
    print("-----------")
    for key, meta in SCRAPE_TARGETS.items():
        extra = " (paginated)" if meta["supports_pages"] else ""
        print(f"- {meta['name']} [{key}]{extra}")
    site = input("Choose site key: ").strip()
    if site not in SCRAPE_TARGETS:
        raise SystemExit("Unknown site.")
    out = input("Output file (.csv or .json): ").strip()
    if not (out.endswith(".csv") or out.endswith(".json")):
        raise SystemExit("Output must end with .csv or .json")
    pages = SCRAPE_TARGETS[site]["default_pages"]
    if SCRAPE_TARGETS[site]["supports_pages"]:
        raw = input(f"Pages [{pages}]: ").strip()
        if raw:
            pages = max(1, int(raw))
    delay = 0.8
    rawd = input(f"Delay seconds [{delay}]: ").strip()
    if rawd:
        delay = max(0.0, float(rawd))
    return site, out, pages, delay

def main():
    args = parse_args()
    pages = args.pages or SCRAPE_TARGETS[args.site]["default_pages"]
    run_scrape(args.site, args.out, pages, args.delay)
if __name__ == "__main__":
    main()