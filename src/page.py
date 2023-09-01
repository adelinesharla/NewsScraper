from abc import ABC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class Page(ABC):
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
