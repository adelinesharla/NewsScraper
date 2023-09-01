from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utils import resilient_action
from page import Page
import logging

logger = logging.getLogger(__name__)


class ResultPage(Page):
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
    SECTION_BUTTON = "sectionfilter"
    SECTION_SELECTION = "button[data-testid='Select-Popup']"
    SECTION_LIST = "//select[@name='sectionfilter']"
    SECTION_POPUP = ""

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

    @resilient_action
    def click_category_button(self):
        section_button = self.wait_for(
            EC.element_to_be_clickable,
            (By.ID, self.SECTION_BUTTON),
        )
        if section_button is None:
            raise NoSuchElementException("Category button is None.")
        section_button.click()
        logger.info("Successfully clicked in category button")
        return None

    @resilient_action
    def click_category_selection(self, category):
        section_button = self.wait_for(
            EC.element_to_be_clickable,
            (By.ID, self.SECTION_BUTTON),
        )
        if section_button is None:
            raise NoSuchElementException("Category button is None.")
        section_button.click()
        logger.info("Successfully clicked in category button")

        element = self.wait_for(
            EC.visibility_of_element_located,
            (By.XPATH, self.SECTION_LIST),
        )
        if element is None:
            raise NoSuchElementException("Category select element is None.")
        logger.info("Successfully located select element")

        option = self.wait_for(
            EC.presence_of_element_located,
            (By.XPATH, f"//option[@value='{category.capitalize()}']"),
        )
        if option is None:
            raise NoSuchElementException("Category option element is None.")
        self.browser.driver.execute_script("arguments[0].scrollIntoView();", option)
        option = self.wait_for(
            EC.visibility_of_element_located,
            (By.XPATH, f"//option[@value='{category.capitalize()}']"),
        )
        if option is None:
            raise NoSuchElementException("Category option element is None.")
        logger.info("Successfully located option element")
        # self.browser.driver.execute_script("arguments[0].selected = true;", option)
        element.click()
        logger.info("select click")

        select_element = Select(element)
        select_element.select_by_value(category.capitalize())
        logger.info(f"Successfully select category item '{category.capitalize()}'")
        return None
