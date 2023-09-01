from RPA.Browser.Selenium import Selenium
from selenium.common.exceptions import TimeoutException
from utils import resilient_action
from main_page import MainPage
from result_page import ResultPage
import logging

logger = logging.getLogger(__name__)


class Scraper:
    """Web scraper class for interacting with a website using Selenium.

    This class handles opening a website, searching for a term, retrieving search results,
    and closing the browser.

    Attributes:
        config (dict): Configuration settings for the scraper.
        browser (Selenium): Selenium browser instance.

    Methods:
        open_website(): Opens the specified website.
        search_for_term(term: str): Searches for a term on the website.
        get_search_results(): Retrieves search results.
        close_browser(): Closes all open browser windows.
    TODO:
        - Some news has carrosels or videos instead of images, this is not covered here
        - Fix click_category_selection in result_page to use in search_for_term_by_category
        - Check why some news are not being scrape except for the category
    """

    def __init__(self, config):
        """Initialize Scraper with configuration settings.

        Parameters:
            config (dict): Configuration settings including base_url.
        """
        self.config = config
        self.browser = Selenium()
        self.main_page = MainPage(self.browser, self.config)
        self.result_page = ResultPage(self.browser, self.config)

    @resilient_action
    def open_website(self):
        """Open the website specified in the configuration settings."""
        try:
            self.browser.open_available_browser(self.config["base_url"], headless=True)
            logger.info("Successfully opened the website.")
        # Apearently I dont need to worry on this error always
        except TimeoutException as e:
            logger.warning(f"A potentially non-critical error occurred: {e}")

    def search_for_term_by_category(self, term, category):
        """Search for a term on the website.

        Parameters:
            term (str): The search term to be entered into the search bar.
        """
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
