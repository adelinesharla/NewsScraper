from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from SeleniumLibrary.errors import NoOpenBrowser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from utils import resilient_action


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

    def wait_for(self, condition, *args, **kwargs):
        return WebDriverWait(self.browser.driver, self.config["wait_time"]).until(
            condition(*args), **kwargs
        )

    def find_child_element(self, parent_element, css_selector):
        try:
            return parent_element.find_element(By.CSS_SELECTOR, css_selector)
        except:
            return None

    @resilient_action
    def open_website(self):
        """Open the website specified in the configuration settings."""
        try:
            self.browser.open_available_browser(self.config["base_url"], headless=True)
            if self.browser is None:
                raise NoOpenBrowser
            print("Successfully opened the website.")
        except NoOpenBrowser as e:
            print(f"Error opening browser: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @resilient_action
    def search_for_term(self, term):
        """Search for a term on the website.

        Parameters:
            term (str): The search term to be entered into the search bar.
        """
        try:
            search_button = "button[data-testid='Button']"
            sb_element = self.wait_for(
                EC.presence_of_element_located, (By.CSS_SELECTOR, search_button)
            )

            if sb_element is None:
                print("Search button element is None.")
                return
            sb_element.click()
            print(f"Successfully clicked the search button.")

            input_field = "input[data-testid='FormField:input']"
            input_element = self.wait_for(
                EC.presence_of_element_located, (By.CSS_SELECTOR, input_field)
            )

            if input_element is None:
                print("Input field element is None.")
                return
            input_element.send_keys(term)
            print(f"Successfully entered the search term: {term}")

            self.wait_for(
                EC.text_to_be_present_in_element_value,
                (By.CSS_SELECTOR, input_field),
                term,
            )
            input_element.send_keys(Keys.ENTER)

            div_search = "div[data-testid='StickyRail']"
            self.wait_for(EC.presence_of_element_located, (By.CSS_SELECTOR, div_search))

            search_header = "h1[data-testid='Heading']"
            self.wait_for(
                EC.presence_of_element_located, (By.CSS_SELECTOR, search_header)
            )

            self.wait_for(
                EC.text_to_be_present_in_element_value,
                (By.CSS_SELECTOR, search_header),
                f"Search results for “{term}”",
            )
            print(f"Successfully loaded search results page.")

        except TimeoutException:
            print("Element not found within the specified time.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @resilient_action
    def get_search_results(self):
        """Retrieve and return all search results from multiple pages on the website.

        This method uses Selenium to navigate the website and scrape search results.
        It will automatically handle pagination by clicking the "Next" button until
        the end is reached or the button becomes disabled.

        Returns:
            list: A list of dictionaries containing the scraped data for each search result.
                Each dictionary includes 'title', 'link', 'category', and 'time'.
        """

        all_scraped_data = []
        try:
            while True:
                # Wait for the search results list to appear
                self.wait_for(
                    EC.presence_of_element_located,
                    (By.CSS_SELECTOR, "ul.search-results__list__2SxSK"),
                )
                print("Successfully loaded search results.")

                # Find and iterate over each list item in the search results
                search_results = self.wait_for(
                    EC.presence_of_all_elements_located,
                    (By.CSS_SELECTOR, "li.search-results__item__2oqiX"),
                )

                scraped_data = []
                wait = WebDriverWait(self.browser.driver, self.config["wait_time"])
                for result in search_results:
                    title_element = wait.until(
                        lambda driver: self.find_child_element(
                            result, "h3[data-testid='Heading'] a"
                        )
                    )
                    category_element = wait.until(
                        lambda driver: self.find_child_element(
                            result, "span[data-testid='Label'] span"
                        )
                    )

                    time_element = wait.until(
                        lambda driver: self.find_child_element(
                            result, "time[data-testid='Body']"
                        )
                    )

                    # Store in a dictionary and add to the list of scraped data
                    scraped_data.append(
                        {
                            "title_element": title_element,
                            "link_element": title_element,
                            "category_element": category_element,
                            "time_element": time_element,
                        }
                    )

                all_scraped_data.extend(scraped_data)

                # Check if there's a "Next" button that's not disabled
                self.wait_for(
                    EC.presence_of_element_located,
                    (By.CSS_SELECTOR, "button[aria-label^='Next stories']"),
                ).click()
                print("Successfully retrieved all search results.")
        except TimeoutException:
            print("One of the elements was not found in the specified time.")
        except (NoSuchElementException, WebDriverException):
            print("Reached the end of the pages or encountered an exception.")
        return all_scraped_data

    def close_browser(self):
        """Close all open browser windows."""
        self.browser.close_all_browsers()
        print("Successfully closed all browser windows.")
