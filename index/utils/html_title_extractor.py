from bs4 import BeautifulSoup
import requests


class HtmlTitleExtractor:
    @staticmethod
    def extract_title(url):
        try:
            html_content = requests.get(url).text
            soup = BeautifulSoup(html_content, "html.parser")
            return soup.title.text if soup.title else "No Title Found"
        except Exception as e:
            return f"Error: {str(e)}"
