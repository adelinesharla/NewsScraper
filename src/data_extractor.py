from RPA.Excel.Files import Files
from utils import resilient_action
import re
from requests import get
from uuid import uuid4
import os
import logging


class DataExtractor:
    """A class for extracting and storing data related to news articles.

    Methods:
    --------
    extract_data(search_result: dict) -> dict:
        Extracts relevant data from a given search result.

    store_data_to_excel(data: dict) -> None:
        Stores the extracted data into an Excel file.

        TODO
        Count of search phrases in the title and description
    """

    def __init__(self, excel_file_path=None):
        self.robot_root = os.environ.get("ROBOT_ROOT", ".")
        self.excel_file_path = excel_file_path or os.path.join(
            self.robot_root, "data", "scraped_data.xlsx"
        )
        self.headers = ["title", "money_pattern", "image", "date", "category"]

    def ensure_dir_exists(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def process_image(self, url):
        try:
            response = get(url)
            response.raise_for_status()
            id = uuid4()
            file_path = os.path.join(self.robot_root, "data", f"image_{id}.png")
            file_name = f"image_{id}.png"
            self.ensure_dir_exists(os.path.dirname(file_path))
            with open(file_path, "wb") as f:
                f.write(response.content)
            return file_name
        except Exception as e:
            logging.error(f"Failed to download image: {e}")
            raise e

    def contains_money_patterns(self, input_str):
        patterns = [
            r"\$\d+\.\d{2}",  # $xx.x
            r"\$\d{1,3}(?:,\d{3})*\.\d{2}",  # $xxx,xxx.xx
            r"\d+ dollars",  # xx dollars
            r"\d+ USD",  # xx USD
        ]

        compound_pattern = "|".join(patterns)

        if re.search(compound_pattern, input_str):
            return True
        else:
            return False

    @resilient_action
    def extract_data(self, search_result):
        """Extract relevant data from a given search result.

        Parameters:
        -----------
        search_result : dict
            A dictionary containing the HTML elements or data of a search result.

        Returns:
        --------
        dict
            A dictionary containing the extracted data, such as title, date, and description.
        """
        extracted_data = {}
        title_element = search_result.get("title_element")
        time_element = search_result.get("time_element")
        category_element = search_result.get("category_element")
        image_element = search_result.get("image_element")

        if title_element:
            extracted_data["title"] = title_element.text
            extracted_data["money_pattern"] = self.contains_money_patterns(
                extracted_data["title"]
            )
        if image_element:
            filename = self.process_image(image_element.get_attribute("src"))
            extracted_data["image"] = filename
        if time_element:
            extracted_data["date"] = time_element.get_attribute("datetime")
        if category_element:
            extracted_data["category"] = category_element.text
        return extracted_data

    @resilient_action
    def store_data_to_excel(self, data):
        """Store the extracted data into an Excel file.

        Parameters:
        -----------
        data : dict
            A dictionarie of the extracted data.

        Returns:
        --------
        None
        """
        self.ensure_dir_exists(os.path.dirname(self.excel_file_path))

        excel = Files()
        try:
            if os.path.exists(self.excel_file_path):
                excel.open_workbook(self.excel_file_path)
                excel.get_active_worksheet()
                excel.append_rows_to_worksheet([data])
            else:
                excel.create_workbook(self.excel_file_path)
                excel.get_active_worksheet()
                # Fill headers
                for col, header in enumerate(self.headers, start=1):
                    excel.set_cell_value(1, col, header)

                # Fill data
                for col, key in enumerate(data.keys(), start=1):
                    excel.set_cell_value(2, col, data[key])

            excel.save_workbook()
            excel.close_workbook()
        except Exception as e:
            logging.error(f"An error occurred while saving to Excel: {e}")
            raise e
