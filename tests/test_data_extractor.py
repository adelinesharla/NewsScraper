import unittest
from unittest.mock import patch
from src.data_extractor import DataExtractor


class MockElement:
    def __init__(self, text=None, href=None, datetime=None):
        self.text = text
        self.href = href
        self.datetime = datetime

    def get_attribute(self, name):
        return getattr(self, name, None)


class TestDataExtractor(unittest.TestCase):
    def setUp(self):
        self.data_extractor = DataExtractor(
            term="apple", category="Business", month_number=2
        )

    @patch("src.data_extractor.get")
    def test_extract_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"fake_img_data"
        mock_search_result = {
            "title_element": MockElement(text="Apple announces new iPhone"),
            "image_element": MockElement(href="http://image.url"),
            "time_element": MockElement(datetime="2023-07-10T20:00:00Z"),
            "category_element": MockElement(text="Business"),
        }
        result = self.data_extractor.extract_data(mock_search_result)
        self.assertIsNotNone(result)

    def test_extract_data_date_out_of_range(self):
        mock_search_result = {
            "time_element": MockElement(datetime="2022-01-10T20:00:00Z")
        }
        result = self.data_extractor.extract_data(mock_search_result)
        self.assertIsNone(result)

    @patch("src.data_extractor.Files")
    def test_store_data_to_excel_success(self, mock_files):
        mock_excel = mock_files.return_value
        mock_excel.open_workbook.return_value = None
        mock_excel.get_active_worksheet.return_value = None
        mock_excel.append_rows_to_worksheet.return_value = None
        mock_excel.save_workbook.return_value = None
        mock_excel.close_workbook.return_value = None

        mock_data = {
            "money_pattern": False,
            "count_term": 1,
            "title": "Some title",
            "image": "Some image",
            "date": "2023-07-10",
        }
        try:
            self.data_extractor.store_data_to_excel(mock_data)
        except Exception as e:
            self.fail(f"store_data_to_excel raised an exception: {e}")

    @patch("src.data_extractor.Files")
    def test_store_data_to_excel_failure(self, mock_files):
        mock_excel = mock_files.return_value
        mock_excel.open_workbook.side_effect = Exception("Excel Error")

        mock_data = {
            "money_pattern": False,
            "count_term": 1,
            "title": "Some title",
            "image": "Some image",
            "date": "2023-07-10",
        }

        with self.assertRaises(Exception):
            self.data_extractor.store_data_to_excel(mock_data)


if __name__ == "__main__":
    unittest.main()
