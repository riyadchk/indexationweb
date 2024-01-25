import urllib.request
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
import time
import xml.etree.ElementTree as ET
import sqlite3
import concurrent.futures


class WebCrawler:
    def __init__(self, start_url, max_urls=50, max_links_per_page=5):
        self.start_url = start_url
        self.visited_urls = set()
        self.urls_to_crawl = [start_url]
        self.crawled_urls = []
        self.max_urls = max_urls
        self.max_links_per_page = max_links_per_page
        self.last_download_time = time.time()

    def crawl(self):
        self.read_sitemap(self.start_url)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while self.urls_to_crawl and len(self.crawled_urls) < self.max_urls:
                url = self.get_next_url()
                if url and self.can_crawl(url):
                    executor.submit(self.download_and_find_links, url)
                    time.sleep(max(0, 5 - (time.time() - self.last_download_time)))
        self.write_crawled_urls()

    def get_next_url(self):
        if self.urls_to_crawl:
            url = self.urls_to_crawl.pop(0)
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                self.crawled_urls.append(url)
                return url
        return None

    def read_sitemap(self, url):
        try:
            response = urllib.request.urlopen(urllib.parse.urljoin(url, "/sitemap.xml"))
            tree = ET.ElementTree(file=response)
            for elem in tree.iter(tag="loc"):
                self.urls_to_crawl.append(elem.text)
        except urllib.error.HTTPError as e:
            print(f"Error reading sitemap: {e}")

    def can_crawl(self, url):
        rp = RobotFileParser()
        rp.set_url(urllib.parse.urljoin(url, "/robots.txt"))
        rp.read()
        return rp.can_fetch("*", url)

    def download_and_find_links(self, url):
        self.download_page(url)
        self.find_links(url)

    def download_page(self, url):
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                self.last_download_time = time.time()
                self.store_page_with_new_connection(url)
        except urllib.error.URLError as e:
            print(f"Error downloading page {url}: {e}")

    def store_page_with_new_connection(self, url):
        try:
            conn = sqlite3.connect("webpages.db")
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS webpages
                   (url text, timestamp real)"""
            )
            cursor.execute("INSERT INTO webpages VALUES (?, ?)", (url, time.time()))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def find_links(self, url):
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                self.process_links(response.read(), url)
        except urllib.error.URLError as e:
            print(f"Error finding links at {url}: {e}")

    def process_links(self, page_content, base_url):
        soup = BeautifulSoup(page_content, "html.parser")
        links = soup.find_all("a")
        count = 0
        for link in links:
            if count >= self.max_links_per_page:
                break
            href = link.get("href")
            if href and href.startswith("http"):
                can_crawl = self.add_url_to_crawl(href)
                count += 1 if can_crawl else 0

    def add_url_to_crawl(self, url):
        if url not in self.visited_urls:
            if self.can_crawl(url):
                self.urls_to_crawl.append(url)
                return True
        return False

    def write_crawled_urls(self):
        with open("crawled_webpages.txt", "w") as file:
            for url in self.crawled_urls:
                file.write(url + "\n")
