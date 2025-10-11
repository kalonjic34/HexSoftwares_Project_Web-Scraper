# HexSoftwares Project - Web Scraper

A modular and extensible Python-based web scraper supporting multiple websites such as **Hacker News** and **Quotes to Scrape**.  
This tool allows you to scrape structured data and export it as **CSV** or **JSON** via **interactive mode** or **command-line usage**.

---

## 🚀 Features

| Capability | Description |
|------------|-------------|
| ✅ Interactive Menu | Run without arguments and follow prompts. |
| ✅ CLI Support | Automate scraping with command-line flags. |
| ✅ Pagination Support | Built-in page iteration for quote scraping. |
| ✅ Delay Handling | Prevents rate limiting or block by websites. |
| ✅ CSV / JSON Export | Flexible data output options. |

---

## 📂 Project Structure

```

HexSoftwares_Project_Web-Scraper/
│── scraper.py          # Main scraper script
│── README.md           # Documentation (you are here)
└── /output/ (optional) # Suggested directory to store results

````

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/kalonjic34/HexSoftwares_Project_Web-Scraper.git
cd HexSoftwares_Project_Web-Scraper
````

2. Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## 🧪 Usage

### ✅ Option A: Interactive Mode

Simply run:

```bash
python scraper.py
```

You'll be prompted to choose:

```
Web Scraper
-----------
- Hacker News (front page) [hn]
- Quotes to Scrape (paginated) [quotes]
Choose site key:
```

Then enter:

* Output file: `data.csv` or `data.json`
* Pages (if using `quotes`)
* Delay between requests

---

### ⚙️ Option B: Command-Line Usage

```bash
python scraper.py --site hn --out hn.json
python scraper.py --site quotes --out quotes.csv --pages 5 --delay 1.0
```

| Argument  | Description                                   | Example             |
| --------- | --------------------------------------------- | ------------------- |
| `--site`  | `hn` or `quotes`                              | `--site hn`         |
| `--out`   | Output filename (ending in `.csv` or `.json`) | `--out results.csv` |
| `--pages` | Number of pages (only for `quotes`)           | `--pages 3`         |
| `--delay` | Delay in seconds between requests             | `--delay 1.2`       |

---

## 📁 Output Format

### Hacker News Example (`hn`)

```json
{
  "rank": 1,
  "title": "Example Post",
  "url": "https://example.com",
  "site": "example.com",
  "points": 120,
  "author": "someuser",
  "comments": 45
}
```

### Quotes Example (`quotes`)

```json
{
  "text": "“The world as we have created it...”",
  "author": "Albert Einstein",
  "tags": ["change", "deep-thoughts", "thinking"]
}
```

---

## 🔧 Future Improvements (Planned or Suggested)

* [ ] Add support for **more websites**
* [ ] Parallel fetching with **asyncio**
* [ ] GUI version using **Tkinter or PySimpleGUI**
* [ ] Docker container for simplified deployment

---

## 🤝 Contributing

Pull requests are welcome! If you'd like to add a new scraping target:

1. Define a parser function.
2. Add it to `SCRAPE_TARGETS` in `scraper.py`.
3. Test via both CLI and interactive mode.

---

## 📜 License

This project is currently **unlicensed**.
If you want, I can add **MIT License** or **Apache 2.0** — just say the word.

---

Happy scraping! 🕸️✨
Maintained by **[@kalonjic34](https://github.com/kalonjic34)**
