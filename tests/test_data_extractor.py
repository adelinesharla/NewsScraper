import pytest
from RPA.Browser.Selenium import Selenium
from src.data_extractor import DataExtractor
from pandas.testing import assert_frame_equal
import pandas as pd
import os

# Mock HTML element class for testing
class MockElement:
    def __init__(self, text=None, href=None, datetime=None):
        self.text = text
        self.href = href
        self.datetime = datetime

    def get_attribute(self, name):
        return getattr(self, name, None)

class TestDataExtractor:
    @pytest.fixture
    def setup_extractor(self):
        extractor = DataExtractor()
        yield extractor

    def _test_extract_data_success(self, setup_extractor):
        # Note that in a real test you'd mock these to behave like actual HTML elements
        sample_result = {
            "title_element": MockElement(text="Example"),
            "link_element": MockElement(href="https://example.com"),
            "date_element": MockElement(datetime="2023-01-01"),
            "description_element": MockElement(text="Some description")
        }
        
        extracted_data = setup_extractor.extract_data(sample_result)
        
        assert extracted_data, "No data was extracted."
        assert "title" in extracted_data, "Extracted data does not contain 'title'"
        assert "link" in extracted_data, "Extracted data does not contain 'link'"
        assert "date" in extracted_data, "Extracted data does not contain 'date'"
        assert "description" in extracted_data, "Extracted data does not contain 'description'"

    def test_store_data_to_excel_success(self, setup_extractor):
        # Ensure the directory exists
        if not os.path.exists("../data"):
            os.makedirs("../data")
        sample_data = [
            {"title": "Title1", "link": "Link1", "category": "Cat1", "time": "Time1"},
            {"title": "Title2", "link": "Link2", "category": "Cat2", "time": "Time2"},
        ]

        setup_extractor.store_data_to_excel(sample_data)

        assert os.path.exists("../data/scraped_data.xlsx"), "Excel file was not created."

        read_data = pd.read_excel("../data/scraped_data.xlsx")
        expected_data = pd.DataFrame(sample_data)
        
        assert_frame_equal(read_data, expected_data, check_like=True)

        # Clean up
        os.remove("../data/scraped_data.xlsx")