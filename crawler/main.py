from crawler import WebCrawler


def main():
    start_url = "https://ensai.fr/"

    crawler = WebCrawler(start_url, max_urls=20, max_links_per_page=5, verbose=True)
    crawler.crawl()

    print("Crawling completed.")


if __name__ == "__main__":
    main()
