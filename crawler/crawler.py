import urllib.request
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
import time
import xml.etree.ElementTree as ET
import sqlite3
import concurrent.futures
import os
import threading


class WebCrawler:
    """
    A web crawler that downloads webpages and stores them in a database.
    """

    def __init__(self, start_url, max_urls=50, max_links_per_page=5, verbose=False):
        """
        Initialize the WebCrawler object.

        Args:
            start_url (str): The URL to start crawling from.
            max_urls (int): The maximum number of URLs to crawl.
            max_links_per_page (int): The maximum number of links to follow on a page.
            verbose (bool): Whether to print additional information during the crawling process.
        """
        self.start_url = start_url
        self.visited_urls = set()
        self.urls_to_crawl = [start_url]
        self.crawled_urls = []
        self.max_urls = max_urls
        self.max_links_per_page = max_links_per_page
        self.last_download_time = time.time()
        self.verbose = verbose
        self.lock = threading.Lock()
        self.thread_url_map = {}

        # Delete the database file and the crawled_webpages.txt file if they exist
        if os.path.exists("crawler/webpages.db"):
            os.remove("crawler/webpages.db")
        if os.path.exists("crawler/crawled_webpages.txt"):
            os.remove("crawler/crawled_webpages.txt")

    def crawl(self):
        """
        Start the crawling process.
        """
        self.read_sitemap(self.start_url)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while self.urls_to_crawl and len(self.crawled_urls) < self.max_urls:
                url = self.get_next_url()
                if url and self.can_crawl(url):
                    executor.submit(self.download_and_find_links, url)
                    time.sleep(max(0, 5 - (time.time() - self.last_download_time)))
        self.write_crawled_urls()
        if self.verbose:
            self.print_thread_urls()

    def get_next_url(self):
        """
        Get the next URL to crawl.

        Returns:
            str: The next URL to crawl.
        """
        if self.urls_to_crawl:
            with self.lock:
                url = self.urls_to_crawl.pop(0)
                if url not in self.visited_urls:
                    self.visited_urls.add(url)
                    self.crawled_urls.append(url)
                    return url
        return None

    def read_sitemap(self, url):
        """
        Read the sitemap of a website and add the URLs to crawl.

        Args:
            url (str): The URL of the website.
        """
        try:
            response = urllib.request.urlopen(urllib.parse.urljoin(url, "/sitemap.xml"))
            tree = ET.ElementTree(file=response)
            for elem in tree.iter(tag="loc"):
                self.urls_to_crawl.append(elem.text)
        except urllib.error.HTTPError as e:
            print(f"Error reading sitemap: {e}")
            self.find_links(url)

    def can_crawl(self, url):
        """
        Check if a URL can be crawled based on the robots.txt file.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL can be crawled, False otherwise.
        """
        rp = RobotFileParser()
        rp.set_url(urllib.parse.urljoin(url, "/robots.txt"))
        rp.read()
        if self.verbose:
            print(f"Can crawl {url}: {rp.can_fetch('*', url)}")
        return rp.can_fetch("*", url)

    def download_and_find_links(self, url):
        """
        Download a webpage and find links on it.

        Args:
            url (str): The URL of the webpage.
        """
        thread_id = threading.get_ident()
        if thread_id not in self.thread_url_map:
            self.thread_url_map[thread_id] = []
        self.thread_url_map[thread_id].append(url)
        self.download_page(url)
        self.find_links(url)

    def download_page(self, url):
        """
        Download a webpage.

        Args:
            url (str): The URL of the webpage.
        """
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                self.last_download_time = time.time()
                if self.verbose:
                    print(
                        f"Downloading page {url} by thread {os.getpid()} at time {self.last_download_time}"
                    )
                self.store_page_with_new_connection(url)
        except urllib.error.URLError as e:
            print(f"Error downloading page {url}: {e}")

    def store_page_with_new_connection(self, url):
        """
        Store a webpage in the database.

        Args:
            url (str): The URL of the webpage.
        """
        try:
            conn = sqlite3.connect("crawler/webpages.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS webpages (url text, age real)")
            cursor.execute("INSERT INTO webpages VALUES (?, ?)", (url, time.time()))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def find_links(self, url):
        """
        Find links on a webpage.

        Args:
            url (str): The URL of the webpage.
        """
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                self.process_links(response.read(), url)
        except urllib.error.URLError as e:
            print(f"Error finding links at {url}: {e}")

    def process_links(self, page_content, base_url):
        """
        Process the links on a webpage.

        Args:
            page_content (str): The content of the webpage.
            base_url (str): The base URL of the webpage.
        """
        soup = BeautifulSoup(page_content, "html.parser")
        links = soup.find_all("a")
        if self.verbose:
            print(f"Found {len(links)} links on page {base_url}")
        count = 0
        for link in links:
            if count >= self.max_links_per_page:
                break
            href = link.get("href")
            if href and href.startswith("http"):
                can_crawl = self.add_url_to_crawl(href)
                count += 1 if can_crawl else 0

    def add_url_to_crawl(self, url):
        """
        Add a URL to the list of URLs to crawl.

        Args:
            url (str): The URL to add.

        Returns:
            bool: True if the URL was added, False otherwise.
        """
        if url not in self.visited_urls:
            with self.lock:
                if self.can_crawl(url):
                    self.urls_to_crawl.append(url)
                    return True
        return False

    def write_crawled_urls(self):
        """
        Write the crawled URLs to a file.
        """
        with open("crawler/crawled_webpages.txt", "w") as file:
            for url in self.crawled_urls:
                file.write(url + "\n")

    def print_thread_urls(self):
        """
        Print the visited URLs for each thread.
        """
        for thread_id, urls in self.thread_url_map.items():
            print(f"Thread {thread_id} visited URLs: {urls}")
