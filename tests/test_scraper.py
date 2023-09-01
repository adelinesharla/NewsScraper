import unittest
from unittest.mock import patch, Mock
from src.scraper import Scraper
from selenium.common.exceptions import TimeoutException


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.config = {"base_url": "https://example.com"}
        self.scraper = Scraper(self.config)

    @patch("src.scraper.MainPage")
    @patch("src.scraper.ResultPage")
    def test_search_for_term_by_category(self, MockResultPage, MockMainPage):
        # Test for success
        self.scraper.search_for_term_by_category("term", "category")
        self.assertTrue(MockMainPage.verify_search_button.called)
        self.assertTrue(MockMainPage.click_search_button.called)
        self.assertTrue(MockMainPage.input_search_field.called)
        self.assertTrue(MockMainPage.click_to_search.called)

        # Test for failure (let's say verify_search_button raises an exception)
        MockMainPage.verify_search_button.side_effect = TimeoutException()
        with self.assertRaises(TimeoutException):
            self.scraper.search_for_term_by_category("term", "category")

    @patch("src.scraper.ResultPage")
    def test_scrape_news(self, MockResultPage):
        # Test for success
        result = Mock()
        number_news = 5
        output = self.scraper.scrape_news(result, number_news)
        self.assertIsInstance(output, dict)

        # Test for failure (let's say verify_item raises an exception)
        MockResultPage.verify_item.side_effect = TimeoutException()
        with self.assertRaises(TimeoutException):
            self.scraper.scrape_news(result, number_news)

    @patch("src.scraper.ResultPage")
    def test_go_to_next_page(self, MockResultPage):
        # Test for success
        output = self.scraper.go_to_next_page()
        self.assertTrue(MockResultPage.click_next_button.called)

        # Test for failure (let's say click_next_button raises an exception)
        MockResultPage.click_next_button.side_effect = TimeoutException()
        with self.assertRaises(TimeoutException):
            self.scraper.go_to_next_page()


if __name__ == "__main__":
    unittest.main()
