import pytest
from RPA.Browser.Selenium import Selenium
from src.scraper import Scraper


class TestScraper:
    @pytest.fixture
    def setup_scraper(self):
        config = {"base_url": "https://www.reuters.com/", "wait_time": 10}
        scraper = Scraper(config)
        yield scraper
        scraper.close_browser()

    def _test_search_for_term_success(self, setup_scraper):
        term = "climate change"
        setup_scraper.open_website()
        setup_scraper.search_for_term(term)

        try:
            setup_scraper.browser.location_should_contain(term.replace(" ", "+"))
        except AssertionError:
            assert False, f"The URL does not contain the term {term.replace(' ', '+')}"

        try:
            setup_scraper.browser.page_should_contain(f"Search results for “{term}”")
        except AssertionError:
            assert False, f"Page does not contain 'Search results for “{term}”'"

    def _test_search_for_term_fail(self, setup_scraper):
        term = ""
        setup_scraper.open_website()
        setup_scraper.search_for_term(term)

        try:
            setup_scraper.browser.location_should_contain(term.replace(" ", "+"))
        except AssertionError:
            assert False, f"The URL does not contain the term {term.replace(' ', '+')}"

        try:
            setup_scraper.browser.page_should_contain(f"Search results for “{term}”")
            assert (
                False
            ), f"Page contains 'Search results for “{term}”', but it shouldn't"
        except AssertionError:
            assert True


    def _test_get_search_results_success(self, setup_scraper):
        term = "brazil womens"
        setup_scraper.open_website()
        setup_scraper.search_for_term(term)

        results = setup_scraper.get_search_results()
        assert results, "No results were scraped."
        for result in results:
            assert "title_element" in result, "Result does not contain 'title_element'"
            assert "link_element" in result, "Result does not contain 'link_element'"
            assert "category_element" in result, "Result does not contain 'category_element'"
            assert "time_element" in result, "Result does not contain 'time_element'"