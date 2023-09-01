from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from utils import resilient_action
import logging
from page import Page

logger = logging.getLogger(__name__)


class MainPage(Page):
    SEARCH_BUTTON = "button[data-testid='Button']"
    SCROLL_INTO = "arguments[0].scrollIntoView(true);"
    INPUT_FIELD = "input[data-testid='FormField:input']"

    @resilient_action
    def verify_search_button(self):
        sb_element = self.wait_for(
            EC.visibility_of_element_located, (By.CSS_SELECTOR, self.SEARCH_BUTTON)
        )
        if sb_element is None:
            msg = "Search button element is None."
            raise NoSuchElementException(msg)
        self.wait_for(EC.element_to_be_clickable, (By.CSS_SELECTOR, self.SEARCH_BUTTON))

        return sb_element

    @resilient_action
    def click_search_button(self, button):
        self.browser.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.browser.driver.execute_script("arguments[0].click();", button)
        logger.info(f"Successfully clicked the search button.")

    @resilient_action
    def input_search_field(self, term):
        input_element = self.wait_for(
            EC.presence_of_element_located, (By.CSS_SELECTOR, self.INPUT_FIELD)
        )
        if input_element is None:
            msg = "Input field element is None."
            raise NoSuchElementException(msg)
        input_element.send_keys(term)
        logger.info(f"Successfully entered the search term: {term}")
        return input_element

    @resilient_action
    def click_to_search(self, term, input_element):
        self.wait_for(
            EC.text_to_be_present_in_element_value,
            (By.CSS_SELECTOR, self.INPUT_FIELD),
            term,
        )
        input_element.send_keys(Keys.ENTER)
        logger.info(f"Successfully sent the search term: {term}")
