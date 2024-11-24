import re
import requests
import os
import json
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from .model_factory import ModelFactory


class Cache:
    """
    Singleton class for caching URL content.
    """

    _instance = None

    @staticmethod
    def get_instance():
        """
        Get the singleton instance of the cache.
        :return: Cache instance.
        """
        if Cache._instance is None:
            Cache()
        return Cache._instance

    def __init__(self):
        if Cache._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.cache = self.load_cache()
            Cache._instance = self

    CACHE_FILE = "data/cache.json"
    MAX_DEPTH = 2  # Set the maximum recursion depth

    def load_cache(self):
        """
        Load the cached content from a file.
        :return: Cached content as a dictionary.
        """
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        """
        Save the cached content to a file.
        """
        with open(self.CACHE_FILE, "w") as f:
            json.dump(self.cache, f)


class ContentProcessor:
    """
    Facade class for content processing operations such as validating URLs, extracting and encoding content.
    """

    def __init__(self):
        self.cache = Cache.get_instance()

    def validate_url(self, url):
        """
        Check if the URL is valid.
        :param url: URL string.
        :return: Boolean indicating whether the URL is valid.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_all_links(self, url, soup):
        """
        Extract all unique links from the given soup object.
        :param url: Base URL.
        :param soup: BeautifulSoup object.
        :return: Set of unique links.
        """
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urljoin(url, href)
            if (
                self.validate_url(full_url)
                and urlparse(full_url).netloc == urlparse(url).netloc
            ):
                links.add(full_url)
        return links

    def extract_text_from_soup(self, soup):
        """
        Extract meaningful text from the BeautifulSoup object.
        :param soup: BeautifulSoup object.
        :return: Extracted text.
        """
        for element in soup(["script", "style", "header", "footer", "nav", "aside"]):
            element.decompose()
        text = soup.get_text(separator="\n")
        text = re.sub(r"\n\s*\n", "\n\n", text)
        return text

    def crawl_and_extract_content(self, url, visited=set(), depth=0):
        """
        Recursively crawl and extract content from the help website.
        :param url: URL to crawl.
        :param visited: Set of visited URLs to avoid cycles.
        :param depth: Current depth of recursion.
        :return: Extracted content and corresponding URLs.
        """
        if url in visited or depth > Cache.MAX_DEPTH:
            return "", []

        if url in self.cache.cache:
            print(f"Using cached content for URL: {url}")
            return self.cache.cache[url]["content"], self.cache.cache[url]["urls"]

        print(
            f"Crawling URL: {url}, Depth: {depth}"
        )  # Debug statement to show the crawling progress
        visited.add(url)

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return "", []

        soup = BeautifulSoup(response.text, "html.parser")
        content = self.extract_text_from_soup(soup)
        urls = [url] * len(content.split("\n"))

        # Recursively crawl and extract content from all linked pages
        if depth < Cache.MAX_DEPTH:
            links = self.get_all_links(url, soup)
            for link in links:
                sub_content, sub_urls = self.crawl_and_extract_content(
                    link, visited, depth + 1
                )
                content += sub_content
                urls += sub_urls

        self.cache.cache[url] = {"content": content, "urls": urls}
        self.cache.save_cache()

        return content, urls

    def index_content(self, content):
        """
        Index the extracted content for efficient querying.
        :param content: The raw text content extracted from the documentation.
        :return: A dictionary with indexed content.
        """
        index = defaultdict(list)
        for i, line in enumerate(content.split("\n")):
            if line.strip():  # Only index non-empty lines
                index["lines"].append((i, line.strip()))
        return index

    def encode_content(self, index):
        """
        Encode the indexed content using a sentence transformer model.
        :param index: The indexed content.
        :return: Encoded content and the corresponding text.
        """
        texts = [line for _, line in index["lines"]]
        sentence_model = ModelFactory.get_sentence_model()
        embeddings = sentence_model.encode(texts, convert_to_tensor=True)
        return embeddings, texts
