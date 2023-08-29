from RPA.Browser.Selenium import Selenium
from .utils import resilient_action


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
    """

    def __init__(self, config):
        """Initialize Scraper with configuration settings.

        Parameters:
            config (dict): Configuration settings including base_url.
        """
        self.config = config
        self.browser = Selenium()

    @resilient_action
    def open_website(self):
        """Open the website specified in the configuration settings."""
        self.browser.open_available_browser(self.config["base_url"])

    @resilient_action
    def search_for_term(self, term):
        """Search for a term on the website.

        Parameters:
            term (str): The search term to be entered into the search bar.
        """
        # Click the button to open the search bar
        search_button = "button[aria-label='Open search bar']"
        self.browser.click_element(search_button)

        # Now enter the search term in the input field and press ENTER
        input_field = "#react-aria8902221257-\\:r8\\:"
        self.browser.input_text(input_field, term)
        self.browser.press_keys(input_field, "ENTER")

    @resilient_action
    def get_search_results(self):
        """Retrieve search results from the website.

        Note: Implementation of scraping logic is needed.
        """
        # implement your scraping logic here
        pass

    def close_browser(self):
        """Close all open browser windows."""
        self.browser.close_all_browsers()
