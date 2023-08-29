import pytest
from RPA.Browser.Selenium import Selenium
from src.scraper import Scraper


class TestScraper:
    @pytest.fixture
    def setup_scraper(self):
        config = {"base_url": "https://www.reuters.com/"}
        scraper = Scraper(config)
        yield scraper
        scraper.close_browser()

    def test_search_for_term_success(self, setup_scraper):
        term = "climate change"
        setup_scraper.open_website()
        setup_scraper.search_for_term(term)

        assert True, setup_scraper.browser.location_should_contain(term.replace(" ", "-"))
        assert True, setup_scraper.browser.page_should_contain('.search-results__heading')

    def test_search_for_term_fail(self, setup_scraper):
        term = ""
        setup_scraper.open_website()
        setup_scraper.search_for_term(term)
        
        assert True, setup_scraper.browser.location_should_contain(term.replace(" ", "-"))
        assert False, setup_scraper.browser.page_should_contain('.search-results__heading')
