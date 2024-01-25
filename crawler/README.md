# Minimal Web Crawler Project

## *Riyad Chamekh*

## Overview

This Web Crawler is a Python-based tool designed to crawl websites, starting from a given URL. It systematically browses the web and stores crawled URLs in a database, following specific constraints like maximum number of URLs to crawl and maximum number of links per page.

### Features

- Reads sitemaps to discover URLs.
- Respects `robots.txt` for crawling rules and waiting time between downloads.
- Limits the number of URLs to crawl.
- Restricts the number of links processed per page.
- Stores crawled URLs in an SQLite database.
- Uses concurrent threads for efficient crawling.

## Getting Started

### Prerequisites

- Python 3.x
- Libraries: `urllib`, `bs4` (BeautifulSoup), `sqlite3`, `concurrent.futures`, `os`

You can install the required packages using pip:

```bash
pip install beautifulsoup4 
```

### Installation

1. Clone the repository or download the source code.
2. Ensure Python 3.x is installed on your system.

### Usage

To use the Web Crawler, navigate to the directory containing `main.py` and run:

```bash
python main.py
```

### Configuration

You can configure the crawler by modifying the parameters in `main.py`:

- `start_url`: The initial URL from where the crawler will start.
- `max_urls`: The maximum number of URLs to crawl.
- `max_links_per_page`: The maximum number of links to process on each page.
- `verbose`: Get more informations during the crawling process.

## Files Description

- `crawler.py`: Contains the `WebCrawler` class responsible for the crawling logic.
- `main.py`: The entry point of the program, where you can set the starting URL and other parameters.
- `webpages.db`: SQLite database file where crawled URLs are stored.
- `crawled_webpages.txt`: A text file containing the list of crawled URLs.
