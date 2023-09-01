from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utils import resilient_action
import logging

logger = logging.getLogger(__name__)


class ResultPage:
    DIV_SEARCH = "div[data-testid='StickyRail']"
    SEARCH_HEADER = "h1[data-testid='Heading']"
    UL = "ul.search-results__list__2SxSK"
    IL = "li.search-results__item__2oqiX"
    TITLE_ITEM = "h3[data-testid='Heading'] a"
    CATEGORY_ITEM = "span[data-testid='Label'] span"
    TIME_ITEM = "time[data-testid='Body']"
    IMAGE_ITEM = "img"
    DIV_IMAGE_ITEM = "div[data-testid='Image']"
    NEXT_BUTTON = "button[aria-label^='Next stories']"

    def __init__(self, browser, config):
        self.browser = browser
        self.config = config

    def wait_for(self, condition, *args, **kwargs):
        return WebDriverWait(self.browser.driver, self.config["wait_time"]).until(
            condition(*args), **kwargs
        )

    def try_wait_for_element(self, condition, element, news):
        try:
            web_element = WebDriverWait(
                self.browser.driver, self.config["wait_time"]
            ).until(condition)
            return web_element
        except TimeoutException:
            logger.warning(
                f"The {element} of the news number {news}, was not able to be scraped"
            )
            return None

    def find_child_element(self, parent_element, locator, selector=None):
        try:
            if selector is None:
                return parent_element.find_element(By.CSS_SELECTOR, locator)
            else:
                return parent_element.find_element(selector, locator)
        except NoSuchElementException:
            return None

    @resilient_action
    def verify_results(self):
        self.wait_for(
            EC.presence_of_element_located, (By.CSS_SELECTOR, self.DIV_SEARCH)
        )
        logger.info(f"Successfully loaded results box")
        head_element = self.wait_for(
            EC.presence_of_element_located, (By.CSS_SELECTOR, self.SEARCH_HEADER)
        )
        if head_element is None:
            raise NoSuchElementException("Search header element is None.")
        logger.info(f"Successfully located header results box")
        self.wait_for(EC.visibility_of, head_element)
        logger.info(f"Successfully loaded search results page.")

        return None

    def click_next_button(self):
        try:
            # Check if there's a "Next" button that's not disabled
            next_button = self.wait_for(
                EC.presence_of_element_located,
                (By.CSS_SELECTOR, self.NEXT_BUTTON),
            )
            self.wait_for(
                EC.element_to_be_clickable,
                (By.CSS_SELECTOR, self.NEXT_BUTTON),
            )
            if next_button is None:
                logger.info("No next button to click")
                return False
            next_button.click()
            logger.info("clicked next button")
        except TimeoutException:
            logger.info("No next button to click")
            return False
        return True

    @resilient_action
    def verify_item_list(self):
        self.wait_for(
            EC.presence_of_element_located,
            (By.CSS_SELECTOR, self.UL),
        )
        logger.info("Successfully loaded search results.")
        self.wait_for(
            EC.presence_of_all_elements_located,
            (By.CSS_SELECTOR, self.IL),
        )
        logger.info("Successfully located list")
        return None

    @resilient_action
    def get_item_list(self):
        item_results = self.wait_for(
            EC.visibility_of_all_elements_located,
            (By.CSS_SELECTOR, self.IL),
        )
        if item_results is None:
            raise NoSuchElementException("Search item element is None.")
        logger.info("Successfully waited for visible list")
        return item_results

    def verify_item(self, item):
        self.wait_for(EC.visibility_of, item)
        return None

    def get_title_item(self, item, item_number):
        return self.try_wait_for_element(
            lambda driver: self.find_child_element(item, self.TITLE_ITEM),
            "title_element",
            item_number,
        )

    def get_category_item(self, item, item_number):
        return self.try_wait_for_element(
            lambda driver: self.find_child_element(item, self.CATEGORY_ITEM),
            "category_element",
            item_number,
        )

    def get_time_item(self, item, item_number):
        return self.try_wait_for_element(
            lambda driver: self.find_child_element(item, self.TIME_ITEM),
            "time_element",
            item_number,
        )

    def get_image_item(self, item, item_number):
        div_element = self.try_wait_for_element(
            lambda driver: self.find_child_element(item, self.DIV_IMAGE_ITEM),
            "div_element",
            item_number,
        )
        if div_element:
            return self.try_wait_for_element(
                lambda driver: self.find_child_element(
                    div_element, self.IMAGE_ITEM, By.TAG_NAME
                ),
                "image_element",
                item_number,
            )
        return None
