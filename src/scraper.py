from RPA.Browser.Selenium import Selenium
from selenium.common.exceptions import TimeoutException
from utils import resilient_action
from main_page import MainPage
from result_page import ResultPage
import logging

logger = logging.getLogger(__name__)


class Scraper:
    """Automates web scraping tasks for news data.

    This class encapsulates the operations involved in scraping news
    articles from a website. It navigates through pages, locates specific
    elements, and extracts needed data. It is designed to be resilient
    against errors, and uses logging to track its operations.

    Attributes:
        config (dict): Configuration parameters for the scraper.
        browser (Selenium): Browser object to interact with the webpage.
        main_page (MainPage): Object to interact with the main page.
        result_page (ResultPage): Object to interact with the results page.

    Methods:
        open_website(): Open the base website.
        search_for_term_by_category(term, category): Search for news by term and category.
        get_page_results(): Verify and get the list of news items from the results page.
        scrape_news(result, number_news): Extracts the data from a specific news item.
        scrape_page(page): Scrapes all news items on a given page.
        go_to_next_page(): Navigates to the next results page.
        close_browser(): Close all open browser windows.
    """

    def __init__(self, config):
        self.config = config
        self.browser = Selenium()
        self.main_page = MainPage(self.browser, self.config)
        self.result_page = ResultPage(self.browser, self.config)

    @resilient_action
    def open_website(self):
        try:
            self.browser.open_available_browser(self.config["base_url"], headless=True)
            logger.info("Successfully opened the website.")
        # Apearently I dont need to worry on this error always
        except TimeoutException as e:
            logger.warning(f"A potentially non-critical error occurred: {e}")

    def search_for_term_by_category(self, term, category):
        sb_element = self.main_page.verify_search_button()
        self.main_page.click_search_button(sb_element)
        is_element = self.main_page.input_search_field(term)
        self.main_page.click_to_search(term, is_element)
        return None

    @resilient_action
    def get_page_results(self):
        self.result_page.verify_item_list()
        self.result_page.verify_results()
        return self.result_page.get_item_list()

    @resilient_action
    def scrape_news(self, result, number_news):
        self.result_page.verify_item(result)
        title_element = self.result_page.get_title_item(result, number_news)
        category_element = self.result_page.get_category_item(result, number_news)
        time_element = self.result_page.get_time_item(result, number_news)
        image_element = self.result_page.get_image_item(result, number_news)

        # Store in a dictionary and add to the list of scraped data
        return {
            "title_element": title_element,
            "image_element": image_element,
            "category_element": category_element,
            "time_element": time_element,
        }

    def scrape_page(self, page):
        scraped_data = []
        scraped_iterations = len(page)
        for result in page:
            data = self.scrape_news(result, scraped_iterations)
            scraped_data.append(data)
            scraped_iterations -= 1
            logger.info(f"{scraped_iterations} news remaining to scrapy")

        return scraped_data

    def go_to_next_page(self):
        return self.result_page.click_next_button()

    @resilient_action
    def close_browser(self):
        """Close all open browser windows."""
        self.browser.close_all_browsers()
        logger.info("Successfully closed all browser windows.")
